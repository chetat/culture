"""empty message

Revision ID: e9b489936335
Revises: 
Create Date: 2020-07-30 14:22:54.323058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9b489936335'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('release_year', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_movies_release_year'), 'movies', ['release_year'], unique=False)
    op.drop_index('ix_movies_release_date', table_name='movies')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_movies_release_date', 'movies', ['release_date'], unique=False)
    op.drop_index(op.f('ix_movies_release_year'), table_name='movies')
    op.drop_column('movies', 'release_year')
    # ### end Alembic commands ###
