"""initial version

Revision ID: 54729488ac2
Revises: None
Create Date: 2013-04-13 22:32:01.769546

"""

# revision identifiers, used by Alembic.
revision = '54729488ac2'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'list',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.Unicode(), nullable=False),
        sa.Column('stub', sa.Unicode()),
        sa.Column('words', sa.Unicode()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('modified_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        )


def downgrade():
    op.drop_table('list')
