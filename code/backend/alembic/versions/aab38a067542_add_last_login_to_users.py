"""add_last_login_to_users

Revision ID: aab38a067542
Revises: cd92e28a36d2
Create Date: 2025-11-30 20:17:54.637602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aab38a067542'
down_revision: Union[str, Sequence[str], None] = 'cd92e28a36d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Only add the last_login column - SQLite doesn't support most ALTER COLUMN operations
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the last_login column
    op.drop_column('users', 'last_login')
