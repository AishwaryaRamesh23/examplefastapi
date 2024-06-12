"""add content column to smposts table

Revision ID: 3bad4522255b
Revises: cb881ff4dedc
Create Date: 2024-06-11 11:50:50.145004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bad4522255b'
down_revision: Union[str, None] = 'cb881ff4dedc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('smposts',sa.Column('content',sa.String(),nullable=False))
    pass

def downgrade():
    op.drop_column('smposts','content')
    pass
