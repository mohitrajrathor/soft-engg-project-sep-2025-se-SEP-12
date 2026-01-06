"""add doubt tables

Revision ID: 97d274e1aaf2
Revises: a8d851f3b15b
Create Date: 2025-11-26 20:19:50.496935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97d274e1aaf2'
down_revision: Union[str, Sequence[str], None] = 'a8d851f3b15b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create doubt_uploads table
    op.create_table(
        "doubt_uploads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_code", sa.String(length=50), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("created_by_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_doubt_uploads_course_code"),
        "doubt_uploads",
        ["course_code"],
        unique=False,
    )

    # Create doubt_messages table
    op.create_table(
        "doubt_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("upload_id", sa.Integer(), nullable=False),
        sa.Column("author_role", sa.String(length=50), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["upload_id"], ["doubt_uploads.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_doubt_messages_upload_id"),
        "doubt_messages",
        ["upload_id"],
        unique=False,
    )


def downgrade() -> None:
    # Drop doubt_messages table
    op.drop_index(op.f("ix_doubt_messages_upload_id"), table_name="doubt_messages")
    op.drop_table("doubt_messages")

    # Drop doubt_uploads table
    op.drop_index(op.f("ix_doubt_uploads_course_code"), table_name="doubt_uploads")
    op.drop_table("doubt_uploads")