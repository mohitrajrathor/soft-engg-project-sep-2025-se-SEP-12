"""Add use_latex, publish_mode, and is_published columns to quizzes table.

Revision ID: 7c8f9e0d3a1b
Revises: 97d274e1aaf2
Create Date: 2025-11-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c8f9e0d3a1b'
down_revision = '97d274e1aaf2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to quizzes table
    op.add_column('quizzes', sa.Column('use_latex', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('quizzes', sa.Column('publish_mode', sa.String(length=50), nullable=False, server_default='manual'))
    op.add_column('quizzes', sa.Column('is_published', sa.Boolean(), nullable=False, server_default='0'))
    # Remove the server defaults after the column is created
    op.alter_column('quizzes', 'use_latex', server_default=None)
    op.alter_column('quizzes', 'publish_mode', server_default=None)
    op.alter_column('quizzes', 'is_published', server_default=None)


def downgrade() -> None:
    # Remove the added columns
    op.drop_column('quizzes', 'is_published')
    op.drop_column('quizzes', 'publish_mode')
    op.drop_column('quizzes', 'use_latex')
