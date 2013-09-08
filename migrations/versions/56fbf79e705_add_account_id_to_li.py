"""Add account_id to list

Revision ID: 56fbf79e705
Revises: 4d93f81e7c0
Create Date: 2013-09-07 16:54:04.163852

"""

# revision identifiers, used by Alembic.
revision = '56fbf79e705'
down_revision = '4d93f81e7c0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # XXX(gmwils): Works if an account exists with id=1
    op.add_column('list',
                  sa.Column('account_id',
                            sa.Integer,
                            sa.ForeignKey("account.id", onupdate="CASCADE", ondelete="CASCADE"),
                            nullable=False,
                            server_default='1'))
    op.alter_column('list', 'account_id', server_default=None)


def downgrade():
    op.drop_column('list', 'account_id')
