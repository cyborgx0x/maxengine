"""fiction table

Revision ID: 75393775ac64
Revises: 8f36a02d398a
Create Date: 2021-03-17 18:18:52.470413

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '75393775ac64'
down_revision = '8f36a02d398a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fiction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=300), nullable=True),
    sa.Column('author', sa.Unicode(length=300), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('cover', sa.Text(), nullable=True),
    sa.Column('publish_year', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_engine_post_date_gmt', table_name='engine')
    op.drop_table('engine')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('engine',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('post_title', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=300), nullable=True),
    sa.Column('post_content', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=5000), nullable=True),
    sa.Column('post_date_gmt', mysql.DATETIME(), nullable=True),
    sa.Column('post_excerpt', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=500), nullable=True),
    sa.Column('original_link', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=300), nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='engine_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_engine_post_date_gmt', 'engine', ['post_date_gmt'], unique=False)
    op.drop_table('fiction')
    # ### end Alembic commands ###