"""add_user_id_in_todo_table

Revision ID: 12c84915bab9
Revises: a61389cd92a0
Create Date: 2023-07-02 20:35:24.134594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12c84915bab9'
down_revision = 'a61389cd92a0'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('todos', sa.Column('user_id', sa.Integer))
    op.create_foreign_key(
        "user_todo",
        "todos",
        "users",
        ["user_id"],
        ["id"],
    )

def downgrade() -> None:
    op.drop_constraint("user_todo", "todos", type_="foreignkey")
    op.drop_column("todos", "user_id")