"""add last few columns to posts table

Revision ID: d9fa0cece83a
Revises: e1ba580ad63d
Create Date: 2024-06-11 17:10:14.443154

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'd9fa0cece83a'    # revision identifiers, used by Alembic.
down_revision: Union[str, None] = 'e1ba580ad63d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() :
    op.add_column('smposts',sa.Column('published',sa.Boolean(),nullable=False,server_default='True'))
    op.add_column('smposts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass

def downgrade() :
    op.drop_column('smposts','published')
    op.drop_column('smposts','created_at')
    pass
