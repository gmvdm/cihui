"""Add description to list

Revision ID: 1d8e0b3b949
Revises: 594033d136f
Create Date: 2014-07-20 13:37:41.064387

"""

# revision identifiers, used by Alembic.
revision = '1d8e0b3b949'
down_revision = '594033d136f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('list', sa.Column('description', sa.String, nullable=True))


def downgrade():
    op.drop_column('list', 'description')
