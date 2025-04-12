"""Add transaction_date column to Transaction

Revision ID: c04a49e4c4fb
Revises: 029b403eebba
Create Date: 2025-04-12 10:58:45.146024
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c04a49e4c4fb'
down_revision = '029b403eebba'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add the column as nullable first
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('transaction_date', sa.Date(), nullable=True))

    # Step 2: Backfill current date for existing rows
    op.execute("UPDATE transaction SET transaction_date = CURRENT_DATE WHERE transaction_date IS NULL")

    # Step 3: Alter column to be NOT NULL, specifying full type
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.alter_column(
            'transaction_date',
            existing_type=sa.Date(),
            nullable=False
        )

def downgrade():
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('transaction_date')
