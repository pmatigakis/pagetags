"""Added the Postings model

Revision ID: 1c4fc8c79a04
Revises: 7a8e58f2a158
Create Date: 2016-08-27 16:13:40.907848

"""

# revision identifiers, used by Alembic.
revision = '1c4fc8c79a04'
down_revision = '7a8e58f2a158'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('postings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('added_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['url_id'], ['urls.id'], name='fk_url_id__urls'),
    sa.PrimaryKeyConstraint('id', name='pk_postings')
    )
    op.create_table('posting_tags',
    sa.Column('posting_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['posting_id'], ['postings.id'], name='fk_posting_id__postings'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='fk_tag_id__tags')
    )
    op.drop_table('url_tags')
    op.drop_column(u'urls', 'title')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'urls', sa.Column('title', sa.String(length=256), nullable=False))
    op.create_table('url_tags',
    sa.Column('url_id', sa.INTEGER(), nullable=False),
    sa.Column('tag_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], [u'tags.id'], name=u'fk_tag_id__tags'),
    sa.ForeignKeyConstraint(['url_id'], [u'urls.id'], name=u'fk_url_id__urls')
    )
    op.drop_table('posting_tags')
    op.drop_table('postings')

    ### end Alembic commands ###
