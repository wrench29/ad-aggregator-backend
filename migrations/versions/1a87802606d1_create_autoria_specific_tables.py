"""create autoria specific tables

Revision ID: 1a87802606d1
Revises: d7c92feacb4a
Create Date: 2024-10-06 16:05:19.693338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a87802606d1'
down_revision: Union[str, None] = 'd7c92feacb4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'autoria_ads_count_statistics',
        sa.Column('category_id', sa.Integer, primary_key=True),
        sa.Column('brand_id', sa.Integer, primary_key=True),
        sa.Column('model_id', sa.Integer, primary_key=True),
        sa.Column('ads_count', sa.Integer)
    )
    op.create_table(
        'autoria_price_statistics',
        sa.Column('category_id', sa.Integer, primary_key=True),
        sa.Column('brand_id', sa.Integer, primary_key=True),
        sa.Column('model_id', sa.Integer, primary_key=True),
        sa.Column('min_price', sa.Float),
        sa.Column('max_price', sa.Float)
    )
    op.create_table(
        'autoria_model',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )
    op.create_table(
        'autoria_brand',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )
    op.create_table(
        'autoria_category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )
    with op.batch_alter_table('autoria_ads_count_statistics') as batch_op:
        batch_op.create_foreign_key(
            'fk_autoria_ads_count_statistics_autoria_category',
            'autoria_category',
            ['category_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_autoria_ads_count_statistics_autoria_brand',
            'autoria_brand',
            ['brand_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_autoria_ads_count_statistics_autoria_model',
            'autoria_model',
            ['model_id'],
            ['id']
        )
    with op.batch_alter_table('autoria_price_statistics') as batch_op:
        batch_op.create_foreign_key(
            'fk_autoria_price_statistics_autoria_category',
            'autoria_category',
            ['category_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_autoria_price_statistics_autoria_brand',
            'autoria_brand',
            ['brand_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_autoria_price_statistics_autoria_model',
            'autoria_model',
            ['model_id'],
            ['id']
        )


def downgrade() -> None:
    with op.batch_alter_table('autoria_ads_count_statistics') as batch_op:
        batch_op.drop_constraint(
            'fk_autoria_ads_count_statistics_autoria_model',
            table_name='autoria_ads_count_statistics',
            type_='foreignkey'
        )
        batch_op.drop_constraint(
            'fk_autoria_ads_count_statistics_autoria_brand',
            table_name='autoria_ads_count_statistics',
            type_='foreignkey'
        )
        batch_op.drop_constraint(
            'fk_autoria_ads_count_statistics_autoria_category',
            table_name='autoria_ads_count_statistics',
            type_='foreignkey'
        )
    with op.batch_alter_table('autoria_price_statistics') as batch_op:
        batch_op.drop_constraint(
            'fk_autoria_price_statistics_autoria_model',
            type_='foreignkey'
        )
        batch_op.drop_constraint(
            'fk_autoria_price_statistics_autoria_brand',
            type_='foreignkey'
        )
        batch_op.drop_constraint(
            'fk_autoria_price_statistics_autoria_category',
            type_='foreignkey'
        )

    op.drop_table('autoria_ads_count_statistics')
    op.drop_table('autoria_price_statistics')
    op.drop_table('autoria_model')
    op.drop_table('autoria_brand')
    op.drop_table('autoria_category')
