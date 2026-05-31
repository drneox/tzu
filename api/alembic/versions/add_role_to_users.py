"""Add role column to users

Revision ID: add_role_to_users
Revises: add_control_tags_simple
Create Date: 2025-12-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_role_to_users'
down_revision = 'add_control_tags_simple'
branch_labels = None
depends_on = None


def upgrade():
    # Add role column with default 'reader'
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))

    # Migrate existing admin users: is_admin=True → role='admin'
    op.execute("UPDATE users SET role = 'admin' WHERE is_admin = TRUE")

    # Set all remaining users to 'reader'
    op.execute("UPDATE users SET role = 'reader' WHERE role IS NULL")

    # Make column non-nullable now that data is populated
    op.alter_column('users', 'role', nullable=False, server_default='reader')


def downgrade():
    op.drop_column('users', 'role')
