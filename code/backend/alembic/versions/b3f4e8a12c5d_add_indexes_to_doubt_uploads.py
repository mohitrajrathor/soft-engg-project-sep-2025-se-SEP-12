"""add indexes to doubt uploads for performance

Revision ID: b3f4e8a12c5d
Revises: 97d274e1aaf2
Create Date: 2025-11-30 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f4e8a12c5d'
down_revision: Union[str, Sequence[str], None] = '97d274e1aaf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add composite index for course_code and created_at (for period filtering)
    op.create_index(
        'ix_doubt_uploads_course_code_created_at',
        'doubt_uploads',
        ['course_code', 'created_at'],
        unique=False
    )
    
    # Add index for source filtering
    op.create_index(
        'ix_doubt_uploads_source',
        'doubt_uploads',
        ['source'],
        unique=False
    )


def downgrade() -> None:
    # Drop indexes in reverse order
    op.drop_index('ix_doubt_uploads_source', table_name='doubt_uploads')
    op.drop_index('ix_doubt_uploads_course_code_created_at', table_name='doubt_uploads')
