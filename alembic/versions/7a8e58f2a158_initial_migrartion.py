"""Initial migrartion

Revision ID: 7a8e58f2a158
Revises: 
Create Date: 2016-08-27 15:38:16.574197

"""

# revision identifiers, used by Alembic.
revision = '7a8e58f2a158'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_tags'),
    sa.UniqueConstraint('name', name='uq_tags__name')
    )
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_urls'),
    sa.UniqueConstraint('url', name='uq_urls__url')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_users'),
    sa.UniqueConstraint('username', name='uq_users__username')
    )
    op.create_table('url_tags',
    sa.Column('url_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='fk_tag_id__tags'),
    sa.ForeignKeyConstraint(['url_id'], ['urls.id'], name='fk_url_id__urls')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url_tags')
    op.drop_table('users')
    op.drop_table('urls')
    op.drop_table('tags')
    ### end Alembic commands ###
