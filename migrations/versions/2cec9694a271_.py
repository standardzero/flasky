"""empty message

Revision ID: 2cec9694a271
Revises: e28d0006bde9
Create Date: 2018-06-14 00:43:53.655137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cec9694a271'
down_revision = 'e28d0006bde9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    # ### end Alembic commands ###
