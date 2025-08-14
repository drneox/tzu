"""add_residual_risk_simple

Revision ID: fdc17de72e54
Revises: 05947fa10bba
Create Date: 2025-08-13 21:40:54.809880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdc17de72e54'
down_revision: Union[str, None] = '4a94543a3f82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar solo el campo residual_risk a la tabla risks
    op.add_column('risks', sa.Column('residual_risk', sa.Float(), nullable=True))


def downgrade() -> None:
    # Remover el campo residual_risk
    op.drop_column('risks', 'residual_risk')
