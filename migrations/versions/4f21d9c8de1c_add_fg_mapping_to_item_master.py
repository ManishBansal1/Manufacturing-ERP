"""add fg mapping to item master

Revision ID: 4f21d9c8de1c
Revises: a9b4630ff346
Create Date: 2026-06-21 02:05:12.738352
"""

from alembic import op
import sqlalchemy as sa


revision = '4f21d9c8de1c'
down_revision = 'a9b4630ff346'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table('item_master') as batch_op:

        batch_op.add_column(
            sa.Column(
                'finished_good_id',
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            'fk_item_master_finished_good',
            'finished_goods',
            ['finished_good_id'],
            ['id']
        )


def downgrade():

    with op.batch_alter_table('item_master') as batch_op:

        batch_op.drop_constraint(
            'fk_item_master_finished_good',
            type_='foreignkey'
        )

        batch_op.drop_column(
            'finished_good_id'
        )