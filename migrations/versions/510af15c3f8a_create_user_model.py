"""create user model

Revision ID: 510af15c3f8a
Revises: 6856525bc706
Create Date: 2024-10-07 19:02:52.019989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '510af15c3f8a'
down_revision: Union[str, None] = '6856525bc706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column('username', sa.String, primary_key=True),
        sa.Column('password_hash', sa.String)
    )


def downgrade() -> None:
    op.drop_table("user")
