from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.services.user_service import (
    create_user,
    get_user_by_email,
    verify_password,
    create_password_reset_token,
    get_valid_password_reset,
    mark_password_reset_used,
    update_user_password,
)
from app.schemas.user import UserCreate, UserPublic, Token
from app.models.user import RefreshToken
from app.services.email_service import send_password_reset_email
from app.services.supabase_auth import verify_supabase_jwt


router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8
REFRESH_TOKEN_EXPIRE_DAYS = 30
ALGORITHM = "HS256"
@router.get("/config")
def auth_config():
    if settings.AUTH_PROVIDER == "supabase":
        return {
            "auth_provider": "supabase",
            "supabase_url": settings.SUPABASE_URL,
            "supabase_anon_key": settings.SUPABASE_ANON_KEY,
            "redirect_to": settings.FRONTEND_BASE_URL,
        }
    return {"auth_provider": "local"}



def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": subject, "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": subject, "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_from_token(authorization: Optional[str], db: Session) -> UserPublic:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Yetkilendirme gerekli")
    token = authorization.split(" ", 1)[1]
    # If configured to use Supabase, validate via JWKS and map claims
    if settings.AUTH_PROVIDER == "supabase":
        try:
            claims = verify_supabase_jwt(token)
            email = claims.get("email") or claims.get("sub")
            name = claims.get("user_metadata", {}).get("name") or email
            # Return ad-hoc user (no local DB dependency)
            return UserPublic(id=0, name=name or "User", email=email)
        except Exception:
            raise HTTPException(status_code=401, detail="Geçersiz token")
    # Default local JWT
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Geçersiz token türü")
        email = payload.get("sub")
        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
        return UserPublic.model_validate(user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")


@router.post("/register", response_model=UserPublic)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if settings.AUTH_PROVIDER == "supabase":
        # Registration should be handled on the frontend via Supabase; backend returns 405
        raise HTTPException(status_code=405, detail="Register is handled by Supabase")
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten var")
    created = create_user(db, name=user.name, email=user.email, password=user.password)
    return UserPublic.model_validate(created)


class AdminCreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str


@router.post("/admin/register", response_model=UserPublic)
def admin_register(user: AdminCreateUser):
    # Only allow when service role key is configured
    if not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=403, detail="Admin registration disabled")
    # Call Supabase Admin API to create a user without confirmation
    import requests
    url = f"{settings.SUPABASE_URL}/auth/v1/admin/users"
    headers = {
        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"email": user.email, "password": user.password, "email_confirm": True, "user_metadata": {"name": user.name}}
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    if r.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail=f"Supabase admin create failed: {r.text}")
    data = r.json()
    return UserPublic(id=0, name=data.get('user_metadata', {}).get('name') or user.name, email=data.get('email'))


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if settings.AUTH_PROVIDER == "supabase":
        # Login handled by Supabase on the client; backend does not issue tokens
        raise HTTPException(status_code=405, detail="Login is handled by Supabase")
    # OAuth2PasswordRequestForm fields: username, password
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="E-posta veya şifre hatalı")
    access = create_access_token(subject=user.email)
    refresh = create_refresh_token(subject=user.email)
    # Persist refresh token
    rt = RefreshToken(user_id=user.id, token=refresh)
    db.add(rt)
    db.commit()
    return Token(access_token=access, refresh_token=refresh)


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=Token)
def refresh_token(body: RefreshRequest, db: Session = Depends(get_db)):
    if settings.AUTH_PROVIDER == "supabase":
        raise HTTPException(status_code=405, detail="Refresh is handled by Supabase")
    token_str = body.refresh_token
    try:
        payload = jwt.decode(token_str, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Geçersiz token türü")
        email = payload.get("sub")
        # Check token exists and not revoked
        stored = db.query(RefreshToken).filter(RefreshToken.token == token_str, RefreshToken.revoked == False).first()
        if not stored:
            raise HTTPException(status_code=401, detail="Token iptal edilmiş veya bulunamadı")
        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
        # Rotate refresh token
        stored.revoked = True
        new_refresh = create_refresh_token(subject=user.email)
        db.add(RefreshToken(user_id=user.id, token=new_refresh))
        db.commit()
        new_access = create_access_token(subject=user.email)
        return Token(access_token=new_access, refresh_token=new_refresh)
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")


@router.get("/me", response_model=UserPublic)
def me(authorization: Optional[str] = None, db: Session = Depends(get_db)):
    return get_current_user_from_token(authorization, db)


class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None


@router.post("/logout")
def logout(body: LogoutRequest = None, db: Session = Depends(get_db)):
    # Stateless JWT for access; optionally revoke provided refresh token
    if body and body.refresh_token:
        rt = db.query(RefreshToken).filter(RefreshToken.token == body.refresh_token).first()
        if rt:
            rt.revoked = True
            db.commit()
    return {"status": "ok"}


class PasswordResetRequest(BaseModel):
    email: EmailStr


@router.post("/password-reset/request")
def password_reset_request(body: PasswordResetRequest, db: Session = Depends(get_db)):
    if settings.AUTH_PROVIDER == "supabase":
        # Password reset is handled by Supabase magic link
        raise HTTPException(status_code=405, detail="Password reset is handled by Supabase")
    # Her durumda 200 dönerek bilgi sızmasını engelle
    user = get_user_by_email(db, body.email)
    token = None
    if user:
        token = create_password_reset_token(db, user)
        # E-posta gönder (SMTP yoksa loglanır)
        send_password_reset_email(user.email, token)
    # Production'da token'ı dönmeyiz; burada geliştirme için veriyoruz
    resp = {"status": "ok"}
    if settings.ENVIRONMENT != "production" and token:
        resp["reset_token"] = token
    return resp


class PasswordResetConfirm(BaseModel):
    token: str
    password: str


@router.post("/password-reset/confirm")
def password_reset_confirm(body: PasswordResetConfirm, db: Session = Depends(get_db)):
    if settings.AUTH_PROVIDER == "supabase":
        raise HTTPException(status_code=405, detail="Password reset is handled by Supabase")
    rec = get_valid_password_reset(db, body.token)
    if not rec:
        raise HTTPException(status_code=400, detail="Geçersiz veya süresi dolmuş bağlantı")
    from app.models.user import User as UserModel
    user = db.query(UserModel).filter_by(id=rec.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    update_user_password(db, user, body.password)
    mark_password_reset_used(db, rec)
    return {"status": "ok"}
