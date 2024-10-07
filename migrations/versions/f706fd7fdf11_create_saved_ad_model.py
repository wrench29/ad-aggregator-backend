"""create saved ad model

Revision ID: f706fd7fdf11
Revises: 510af15c3f8a
Create Date: 2024-10-07 20:44:24.140209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f706fd7fdf11'
down_revision: Union[str, None] = '510af15c3f8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "saved_ad",
        sa.Column('username', sa.String, sa.ForeignKey(
            "user.username"), primary_key=True
        ),
        sa.Column('provider', sa.String, sa.ForeignKey(
            "ads.platform"), primary_key=True
        ),
        sa.Column('id', sa.Integer, sa.ForeignKey("ads.id"), primary_key=True),
        sa.Column('save_time', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table("saved_ad")
