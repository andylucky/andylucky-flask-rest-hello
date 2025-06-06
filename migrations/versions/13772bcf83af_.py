"""empty message

Revision ID: 13772bcf83af
Revises: 0710a3208b69
Create Date: 2025-05-13 12:58:39.654382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13772bcf83af'
down_revision = '0710a3208b69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('followers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('follower_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('followed_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('followers_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['followed_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['follower_id'], ['id'])
        batch_op.drop_column('user_id')
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('followers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('followers_user_id_fkey', 'user', ['user_id'], ['id'])
        batch_op.drop_column('followed_id')
        batch_op.drop_column('follower_id')

    # ### end Alembic commands ###
