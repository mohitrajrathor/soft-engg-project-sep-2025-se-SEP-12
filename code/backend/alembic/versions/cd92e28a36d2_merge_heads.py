"""merge_heads

Revision ID: cd92e28a36d2
Revises: 7c8f9e0d3a1b, b3f4e8a12c5d
Create Date: 2025-11-30 20:17:26.795846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd92e28a36d2'
down_revision: Union[str, Sequence[str], None] = ('7c8f9e0d3a1b', 'b3f4e8a12c5d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
