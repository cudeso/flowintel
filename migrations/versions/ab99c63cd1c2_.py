"""empty message

Revision ID: ab99c63cd1c2
Revises: 04ee0d5e0abb
Create Date: 2023-11-29 12:10:42.882375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab99c63cd1c2'
down_revision = '04ee0d5e0abb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('connector__icon', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('connector__icon', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
