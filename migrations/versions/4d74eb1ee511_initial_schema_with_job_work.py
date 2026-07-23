"""Initial schema with job work

Revision ID: 4d74eb1ee511
Revises: a68b27308cfa
Create Date: 2026-07-23 23:54:35.654903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d74eb1ee511'
down_revision = 'a68b27308cfa'
branch_labels = None
depends_on = None


def upgrade():
    # Create new tables first (no constraint issues)
    op.create_table('job_work_receipt',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('receipt_no', sa.String(length=30), nullable=False),
        sa.Column('receipt_date', sa.Date(), nullable=False),
        sa.Column('job_work_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('output_qty_received', sa.Float(), nullable=True),
        sa.Column('output_qty_rejected', sa.Float(), nullable=True),
        sa.Column('scrap_qty_received', sa.Float(), nullable=True),
        sa.Column('job_work_cost', sa.Float(), nullable=True),
        sa.Column('total_cost', sa.Float(), nullable=True),
        sa.Column('remarks', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['job_work_id'], ['job_work_header.id'], name='fk_jw_receipt_jobwork'),
        sa.ForeignKeyConstraint(['location_id'], ['location_master.id'], name='fk_jw_receipt_location'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('receipt_no', name='uq_jw_receipt_no')
    )

    op.create_table('job_work_receipt_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_work_receipt_id', sa.Integer(), nullable=False),
        sa.Column('job_work_detail_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('line_type', sa.String(length=20), nullable=False),
        sa.Column('issued_qty', sa.Float(), nullable=True),
        sa.Column('received_qty', sa.Float(), nullable=True),
        sa.Column('rejected_qty', sa.Float(), nullable=True),
        sa.Column('rate', sa.Float(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('remarks', sa.String(length=250), nullable=True),
        sa.ForeignKeyConstraint(['job_work_detail_id'], ['job_work_detail.id'], name='fk_jw_rd_detail'),
        sa.ForeignKeyConstraint(['item_id'], ['item_master.id'], name='fk_jw_rd_item'),
        sa.ForeignKeyConstraint(['job_work_receipt_id'], ['job_work_receipt.id'], name='fk_jw_rd_receipt'),
        sa.PrimaryKeyConstraint('id')
    )

    # Add location_id to job_work_header using batch with named constraint
    with op.batch_alter_table('job_work_header', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location_id', sa.Integer(), nullable=True))
        # Don't add FK constraint here - do it separately or skip for SQLite
    
    # Add FK separately with explicit name (SQLite compatible)
    with op.batch_alter_table('job_work_header', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_jw_header_location', 'location_master', ['location_id'], ['id'])


def downgrade():
    with op.batch_alter_table('job_work_header', schema=None) as batch_op:
        batch_op.drop_constraint('fk_jw_header_location', type_='foreignkey')
        batch_op.drop_column('location_id')

    op.drop_table('job_work_receipt_detail')
    op.drop_table('job_work_receipt')