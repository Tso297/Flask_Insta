"""empty message

Revision ID: 45ad1ae7c8b9
Revises: 8f8fd10bf7f0
Create Date: 2024-03-23 12:44:34.622778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45ad1ae7c8b9'
down_revision = '8f8fd10bf7f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
