"""create ads table

Revision ID: c8afbd0fb43e
Revises: 
Create Date: 2024-10-04 20:35:36.932344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8afbd0fb43e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ads",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("price", sa.Float),
        sa.Column("name", sa.String),
        sa.Column("model", sa.String),
        sa.Column("brand", sa.String),
        sa.Column("region", sa.String),
        sa.Column("mileage", sa.Float),
        sa.Column("color", sa.String),
        sa.Column("interior", sa.String),
        sa.Column("contacts", sa.String)
    )


def downgrade() -> None:
    op.drop_table("ads")
