"""Added user details

Revision ID: 6a9d6f0d154a
Revises: 
Create Date: 2024-09-14 20:07:53.197852

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6a9d6f0d154a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('middlename', sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column('lastname', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('phone', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('address', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('profilepic', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('birthdate', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('modified_at', sa.DateTime(), nullable=False))
        batch_op.drop_index('username')
        batch_op.create_unique_constraint(None, ['phone'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', mysql.VARCHAR(length=80), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('username', ['username'], unique=True)
        batch_op.drop_column('modified_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('age')
        batch_op.drop_column('birthdate')
        batch_op.drop_column('profilepic')
        batch_op.drop_column('address')
        batch_op.drop_column('phone')
        batch_op.drop_column('lastname')
        batch_op.drop_column('middlename')
        batch_op.drop_column('firstname')

    # ### end Alembic commands ###
