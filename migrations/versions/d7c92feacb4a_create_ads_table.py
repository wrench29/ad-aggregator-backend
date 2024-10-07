"""create ads table

Revision ID: d7c92feacb4a
Revises: 
Create Date: 2024-10-06 16:02:25.026522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7c92feacb4a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ads',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('platform', sa.String, primary_key=True),
        sa.Column('category', sa.String),
        sa.Column('brand', sa.String),
        sa.Column('model', sa.String),
        sa.Column('price', sa.Float),
        sa.Column('region', sa.String),
        sa.Column('mileage', sa.Integer),
        sa.Column('color', sa.String)
    )


def downgrade() -> None:
    op.drop_table('ads')
