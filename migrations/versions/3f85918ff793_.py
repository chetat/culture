"""empty message

Revision ID: 3f85918ff793
Revises: 0fd7a1caa54b
Create Date: 2020-07-20 15:29:59.119086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f85918ff793'
down_revision = '0fd7a1caa54b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_pic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic')
    # ### end Alembic commands ###
