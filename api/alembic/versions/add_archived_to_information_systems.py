"""Add archived to information_systems

Revision ID: add_archived_col
Revises: add_projects_and_members
Create Date: 2026-06-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_archived_col'
down_revision = 'add_projects_and_members'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'information_systems',
        sa.Column('archived', sa.Boolean(), nullable=False, server_default='false')
    )


def downgrade():
    op.drop_column('information_systems', 'archived')
