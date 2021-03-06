"""empty message

Revision ID: da62176990d4
Revises: c00d1a76edb2
Create Date: 2022-06-01 07:53:00.269415

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da62176990d4'
down_revision = 'c00d1a76edb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'upcoming_shows')
    op.drop_column('Venue', 'past_shows')
    op.drop_column('Venue', 'past_shows_count')
    op.drop_column('Venue', 'upcoming_shows_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('upcoming_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('past_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('past_shows', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
