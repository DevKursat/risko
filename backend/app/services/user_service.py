from typing import Optional
from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.models.user import User, RefreshToken, PasswordResetToken


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, name: str, email: str, password: str) -> User:
    user = User(name=name, email=email, password_hash=get_password_hash(password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_password_reset_token(db: Session, user: User, expires_minutes: int = 60) -> str:
    token = secrets.token_urlsafe(48)
    prt = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=expires_minutes),
        used=False,
    )
    db.add(prt)
    db.commit()
    return token


def get_valid_password_reset(db: Session, token: str) -> Optional[PasswordResetToken]:
    rec = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token == token,
            PasswordResetToken.used == False,
            PasswordResetToken.expires_at > datetime.utcnow(),
        )
        .first()
    )
    return rec


def mark_password_reset_used(db: Session, rec: PasswordResetToken):
    rec.used = True
    db.add(rec)
    db.commit()


def update_user_password(db: Session, user: User, new_password: str):
    user.password_hash = get_password_hash(new_password)
    db.add(user)
    db.commit()
