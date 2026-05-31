"""Add audit_logs table

Revision ID: add_audit_logs_table
Revises: add_created_by_to_resources
Create Date: 2026-05-31 00:00:01.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_audit_logs_table'
down_revision = 'add_created_by_to_resources'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('target_user_id', sa.UUID(), nullable=True),
        sa.Column('performed_by_id', sa.UUID(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('detail', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('audit_logs')
