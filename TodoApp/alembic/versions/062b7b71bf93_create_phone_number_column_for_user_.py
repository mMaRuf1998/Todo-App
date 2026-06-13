"""Create Phone Number Column for User table

Revision ID: 062b7b71bf93
Revises: 
Create Date: 2026-06-03 23:55:15.022085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '062b7b71bf93'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
