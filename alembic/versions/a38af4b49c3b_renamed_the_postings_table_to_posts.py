"""Renamed the postings table to posts

Revision ID: a38af4b49c3b
Revises: 1c4fc8c79a04
Create Date: 2016-09-04 01:55:59.408683

"""

# revision identifiers, used by Alembic.
revision = 'a38af4b49c3b'
down_revision = '1c4fc8c79a04'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateSequence, DropSequence, Sequence


def upgrade():
    op.alter_column("posting_tags", "posting_id", new_column_name="post_id")
    op.drop_constraint("fk_posting_id__postings", "posting_tags")

    op.drop_constraint("pk_postings", "postings")
    op.create_primary_key("pk_posts", "postings", ["id"])
    op.execute("ALTER SEQUENCE postings_id_seq RENAME TO posts_id_seq")

    op.create_foreign_key("fk_post_id__posts", "posting_tags", "postings", ["post_id"], ["id"])

    op.rename_table("posting_tags", "post_tags")
    op.rename_table("postings", "posts")


def downgrade():
    op.alter_column("post_tags", "post_id", new_column_name="posting_id")
    op.drop_constraint("fk_post_id__posts", "post_tags")

    op.drop_constraint("pk_posts", "posts")
    op.create_primary_key("pk_postings", "posts", ["id"])
    op.execute("ALTER SEQUENCE posts_id_seq RENAME TO postings_id_seq")

    op.create_foreign_key("fk_posting_id__postings", "post_tags", "posts", ["posting_id"], ["id"])

    op.rename_table("post_tags", "posting_tags")
    op.rename_table("posts", "postings")
