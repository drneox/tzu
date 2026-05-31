"""Add created_by to resources

Revision ID: add_created_by_to_resources
Revises: add_role_to_users
Create Date: 2026-05-31 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_created_by_to_resources'
down_revision = 'add_role_to_users'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('threats', sa.Column('created_by', sa.UUID(), nullable=True))
    op.add_column('information_systems', sa.Column('created_by', sa.UUID(), nullable=True))
    op.add_column('remediations', sa.Column('created_by', sa.UUID(), nullable=True))


def downgrade():
    op.drop_column('remediations', 'created_by')
    op.drop_column('information_systems', 'created_by')
    op.drop_column('threats', 'created_by')
