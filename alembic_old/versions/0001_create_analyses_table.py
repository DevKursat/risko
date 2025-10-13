"""create analyses table

Revision ID: 0001_create_analyses_table
Revises: 
Create Date: 2025-10-12
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_create_analyses_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
        sa.Column('owner_id', sa.String(), nullable=False, index=True),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('earthquake_risk', sa.Float(), nullable=True),
        sa.Column('flood_risk', sa.Float(), nullable=True),
        sa.Column('fire_risk', sa.Float(), nullable=True),
        sa.Column('landslide_risk', sa.Float(), nullable=True),
        sa.Column('overall_risk_score', sa.Float(), nullable=True),
        sa.Column('risk_level', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('analyses')
