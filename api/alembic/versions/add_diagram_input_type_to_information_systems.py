"""Add diagram_input_type to information_systems

Revision ID: add_diagram_input_type
Revises: add_audit_logs_table
Create Date: 2026-05-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'add_diagram_input_type'
down_revision = 'add_audit_logs_table'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'information_systems',
        sa.Column('diagram_input_type', sa.String(), nullable=True)
    )


def downgrade():
    op.drop_column('information_systems', 'diagram_input_type')
