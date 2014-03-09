"""Add Skritter token details

Revision ID: 594033d136f
Revises: 57ca47e70d0
Create Date: 2014-03-09 13:28:11.731526

"""

# revision identifiers, used by Alembic.
revision = '594033d136f'
down_revision = '57ca47e70d0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account', sa.Column('skritter_user_id', sa.String))
    op.add_column('account', sa.Column('skritter_access_token', sa.String))
    op.add_column('account', sa.Column('skritter_refresh_token', sa.String))
    op.add_column('account', sa.Column('skritter_token_expiry', sa.DateTime(),
                                       server_default=sa.text('NOW()')))


def downgrade():
    op.drop_column('account', 'skritter_user_id')
    op.drop_column('account', 'skritter_access_token')
    op.drop_column('account', 'skritter_refresh_token')
    op.drop_column('account', 'skritter_token_expiry')
