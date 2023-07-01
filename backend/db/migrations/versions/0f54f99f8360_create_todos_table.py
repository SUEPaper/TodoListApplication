"""create_todos_table

Revision ID: 0f54f99f8360
Revises: 
Create Date: 2023-07-01 14:49:20.393541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f54f99f8360'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("is_done", sa.Boolean, default=False, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("todos")
