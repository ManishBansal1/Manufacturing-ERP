"""Customer PO links Item Master

Revision ID: 549845b790b4
Revises: 78ac667b067e
"""

from alembic import op
import sqlalchemy as sa

revision = "549845b790b4"
down_revision = "78ac667b067e"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table(
        "customer_po_detail",
        recreate="always"
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "item_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_customer_po_detail_item",
            "item_master",
            ["item_id"],
            ["id"]
        )

        batch_op.drop_column("finished_good_id")


def downgrade():

    with op.batch_alter_table(
        "customer_po_detail",
        recreate="always"
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "finished_good_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_customer_po_detail_fg",
            "finished_goods",
            ["finished_good_id"],
            ["id"]
        )

        batch_op.drop_column("item_id")