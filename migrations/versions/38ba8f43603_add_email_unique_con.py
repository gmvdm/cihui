"""Add email unique constraint

Revision ID: 38ba8f43603
Revises: 56fbf79e705
Create Date: 2013-09-08 08:20:29.220167

"""

# revision identifiers, used by Alembic.
revision = '38ba8f43603'
down_revision = '56fbf79e705'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint('uq_account_email', 'account', ['email'])


def downgrade():
    op.drop_constraint('uq_account_email', 'account')
