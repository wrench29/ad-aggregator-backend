"""create cache info table

Revision ID: da30962003b2
Revises: 1a87802606d1
Create Date: 2024-10-06 16:38:05.308254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da30962003b2'
down_revision: Union[str, None] = '1a87802606d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cache_info',
        sa.Column('data_type', sa.String, primary_key=True),
        sa.Column('last_write', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('cache_info')
