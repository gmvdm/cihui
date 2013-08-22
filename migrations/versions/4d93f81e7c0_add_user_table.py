"""Add account table

Revision ID: 4d93f81e7c0
Revises: 2472bab8a89
Create Date: 2013-08-22 08:13:03.803437

"""

# revision identifiers, used by Alembic.
revision = '4d93f81e7c0'
down_revision = '2472bab8a89'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.Unicode(), nullable=False),
        sa.Column('password_hash', sa.Unicode()),
        sa.Column('password_salt', sa.Unicode()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('modified_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        )


def downgrade():
    op.drop_table('account')
