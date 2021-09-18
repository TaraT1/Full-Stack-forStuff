"""fix: xfer models from app.py to models.py

Revision ID: 2e5162f6f69e
Revises: 4a5fbaa9911b
Create Date: 2021-09-12 21:03:32.562006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e5162f6f69e'
down_revision = '4a5fbaa9911b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Location')
    op.drop_table('Book')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Book',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Book_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('form', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('location_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['Location.id'], name='Book_location_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Book_pkey')
    )
    op.create_table('Location',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Location_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Location_pkey')
    )
    # ### end Alembic commands ###
