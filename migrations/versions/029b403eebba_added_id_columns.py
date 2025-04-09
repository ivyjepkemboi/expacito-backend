from alembic import op
import sqlalchemy as sa

revision = '029b403eebba'
down_revision = '9d06795d3be6'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add nullable 'id' columns
    for table in ['user', 'head', 'category', 'subcategory', 'transaction']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(sa.Column('id', sa.Integer(), nullable=True))

    # Step 2: Populate 'id' columns with unique values
    op.execute("SET @uid := 0")
    op.execute("UPDATE user SET id = (@uid := @uid + 1)")

    op.execute("SET @hid := 0")
    op.execute("UPDATE head SET id = (@hid := @hid + 1)")

    op.execute("SET @cid := 0")
    op.execute("UPDATE category SET id = (@cid := @cid + 1)")

    op.execute("SET @sid := 0")
    op.execute("UPDATE subcategory SET id = (@sid := @sid + 1)")

    op.execute("SET @tid := 0")
    op.execute("UPDATE transaction SET id = (@tid := @tid + 1)")


    # Step 3: Alter columns to be NOT NULL, AUTO_INCREMENT, and UNIQUE
    op.execute("ALTER TABLE user MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT UNIQUE")
    op.execute("ALTER TABLE head MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT UNIQUE")
    op.execute("ALTER TABLE category MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT UNIQUE")
    op.execute("ALTER TABLE subcategory MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT UNIQUE")
    op.execute("ALTER TABLE transaction MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT UNIQUE")


def downgrade():
    for table in ['transaction', 'subcategory', 'category', 'head', 'user']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column('id')
