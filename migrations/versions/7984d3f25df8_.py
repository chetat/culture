"""empty message

Revision ID: 7984d3f25df8
Revises: 1e1d3cd94d43
Create Date: 2020-07-10 09:46:15.583641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7984d3f25df8'
down_revision = '1e1d3cd94d43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albums', sa.Column('album_name', sa.String(), nullable=True))
    op.add_column('books', sa.Column('book_name', sa.String(), nullable=True))
    op.drop_column('books', 'name')
    op.add_column('tracks', sa.Column('song_title', sa.String(), nullable=True))
    op.drop_column('tracks', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tracks', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('tracks', 'song_title')
    op.add_column('books', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('books', 'book_name')
    op.drop_column('albums', 'album_name')
    # ### end Alembic commands ###
