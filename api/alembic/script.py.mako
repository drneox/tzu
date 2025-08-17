<%doc>
    Alembic migration script template.
    This is the default template used by Alembic to generate new migration scripts.
</%doc>

"""
Revision ID: ${up_revision}
Revises: ${', '.join(down_revisions) if down_revisions else None}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = '${up_revision}'
down_revision = ${repr(down_revisions[0]) if down_revisions else None}
branch_labels = ${repr(branch_labels) if branch_labels else None}
depends_on = ${repr(depends_on) if depends_on else None}

def upgrade():
    ${upgrades if upgrades else "    pass"}

def downgrade():
    ${downgrades if downgrades else "    pass"}
