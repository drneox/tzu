"""Add projects and project_members tables, project_id FK on information_systems

Revision ID: add_projects_and_members
Revises: add_diagram_input_type
Create Date: 2026-05-31 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_projects_and_members'
down_revision = 'add_diagram_input_type'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'project_members',
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('added_at', sa.DateTime(), nullable=True),
        sa.Column('added_by', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['added_by'], ['users.id']),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('project_id', 'user_id')
    )
    op.add_column(
        'information_systems',
        sa.Column('project_id', sa.UUID(), nullable=True)
    )
    op.create_foreign_key(
        'fk_is_project',
        'information_systems', 'projects',
        ['project_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    op.drop_constraint('fk_is_project', 'information_systems', type_='foreignkey')
    op.drop_column('information_systems', 'project_id')
    op.drop_table('project_members')
    op.drop_table('projects')
