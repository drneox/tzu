"""Add control_tags to remediations

Revision ID: add_control_tags_simple
Revises: a432de2089d5
Create Date: 2025-09-06 16:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_control_tags_simple'
down_revision = 'a432de2089d5'
branch_labels = None
depends_on = None


def upgrade():
    # Add control_tags column to remediations table
    op.add_column('remediations', sa.Column('control_tags', sa.Text(), nullable=True))


def downgrade():
    # Remove control_tags column from remediations table
    op.drop_column('remediations', 'control_tags')
