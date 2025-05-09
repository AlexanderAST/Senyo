"""fix duration timestamp

Revision ID: 68787b973f71
Revises: 84428e1db320
Create Date: 2025-04-19 23:12:34.147144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '68787b973f71'
down_revision: Union[str, None] = '84428e1db320'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('services', 'duration',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.TIME(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('services', 'duration',
               existing_type=sa.TIME(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    # ### end Alembic commands ###
