"""update autoria models

Revision ID: 0c4641878756
Revises: da30962003b2
Create Date: 2024-10-06 19:23:10.990821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c4641878756'
down_revision: Union[str, None] = 'da30962003b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('autoria_brand') as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.String))
    with op.batch_alter_table('autoria_model') as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.String))
        batch_op.add_column(sa.Column('brand_id', sa.String))


def downgrade() -> None:
    with op.batch_alter_table('autoria_brand') as batch_op:
        batch_op.drop_column(sa.Column('category_id', sa.String))
    with op.batch_alter_table('autoria_model') as batch_op:
        batch_op.drop_column(sa.Column('category_id', sa.String))
        batch_op.drop_column(sa.Column('brand_id', sa.String))
