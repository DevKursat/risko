"""Manually add premium fields to analyses table

Revision ID: 3b2e7616c217
Revises: 
Create Date: 2025-10-13 12:37:18.381843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b2e7616c217'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('analyses', sa.Column('preventive_actions', sa.String(), nullable=True))
    op.add_column('analyses', sa.Column('risk_factors_detail', sa.String(), nullable=True))
    op.add_column('analyses', sa.Column('insurance_guideline', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('analyses', 'insurance_guideline')
    op.drop_column('analyses', 'risk_factors_detail')
    op.drop_column('analyses', 'preventive_actions')