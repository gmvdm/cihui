"""Add public flag

Revision ID: 2472bab8a89
Revises: 54729488ac2
Create Date: 2013-08-17 16:25:50.628769

"""

# revision identifiers, used by Alembic.
revision = '2472bab8a89'
down_revision = '54729488ac2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('list', sa.Column('public', sa.Boolean, nullable=False, server_default='false'))


def downgrade():
    op.drop_column('list', 'public')
