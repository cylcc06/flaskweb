"""empty message

Revision ID: 9c4c207bbcdf
Revises: 15fea399b2fb
Create Date: 2019-03-10 12:47:56.499081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c4c207bbcdf'
down_revision = '15fea399b2fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('test', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_users_test'), 'users', ['test'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_test'), table_name='users')
    op.drop_column('users', 'test')
    # ### end Alembic commands ###
