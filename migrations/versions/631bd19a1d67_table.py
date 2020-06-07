"""table 

Revision ID: 631bd19a1d67
Revises: 
Create Date: 2020-06-06 16:20:43.009230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '631bd19a1d67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_title', sa.Unicode(length=300), nullable=True),
    sa.Column('post_date_gmt', sa.DateTime(), nullable=True),
    sa.Column('post_excerpt', sa.Unicode(length=200), nullable=True),
    sa.Column('original_link', sa.Unicode(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_post_date_gmt'), 'post', ['post_date_gmt'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_post_date_gmt'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###