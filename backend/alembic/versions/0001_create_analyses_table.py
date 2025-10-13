"""create analyses table with rls policies

Revision ID: 0001_create_analyses_table
Revises: 
Create Date: 2025-10-12
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_create_analyses_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('risk_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Add foreign key constraint to auth.users if exists (best-effort)
    try:
        op.create_foreign_key(
            'fk_analyses_user_id_auth_users',
            'analyses',
            'auth.users',
            ['user_id'],
            ['id'],
            ondelete='SET NULL'
        )
    except Exception:
        # If auth schema or users table doesn't exist, skip FK creation
        pass

    # Enable RLS on analyses
    op.execute("ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;")

    # Create SELECT policy (users can only select rows where auth.uid() = user_id)
    op.execute("""
    CREATE POLICY "Kullanıcılar yalnızca kendi analizlerini görebilir"
    ON public.analyses
    FOR SELECT
    USING (auth.uid() = user_id);
    """)

    # Create INSERT policy (users can insert if auth.uid() = user_id or user_id IS NULL)
    op.execute("""
    CREATE POLICY "Kullanıcılar analiz ekleyebilir"
    ON public.analyses
    FOR INSERT
    WITH CHECK ((auth.uid() = user_id) OR (user_id IS NULL));
    """)


def downgrade() -> None:
    # Drop policies and table on downgrade
    op.execute('DROP POLICY IF EXISTS "Kullanıcılar analiz ekleyebilir" ON public.analyses;')
    op.execute('DROP POLICY IF EXISTS "Kullanıcılar yalnızca kendi analizlerini görebilir" ON public.analyses;')
    op.execute('ALTER TABLE public.analyses DISABLE ROW LEVEL SECURITY;')
    op.drop_table('analyses')
