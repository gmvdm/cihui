"""Add a name to account

Revision ID: 57ca47e70d0
Revises: 38ba8f43603
Create Date: 2014-03-01 17:08:04.511596

"""

# revision identifiers, used by Alembic.
revision = '57ca47e70d0'
down_revision = '38ba8f43603'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account', sa.Column('name', sa.String))


def downgrade():
    op.drop_column('account', 'name')
