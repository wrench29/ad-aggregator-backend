"""add period the ad count model

Revision ID: 6856525bc706
Revises: 0c4641878756
Create Date: 2024-10-06 19:55:18.588361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6856525bc706'
down_revision: Union[str, None] = '0c4641878756'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('autoria_ads_count_statistics') as batch_op:
        batch_op.add_column(sa.Column('period', sa.Integer))


def downgrade() -> None:
    with op.batch_alter_table('autoria_ads_count_statistics') as batch_op:
        batch_op.drop_column(sa.Column('period', sa.Integer))
