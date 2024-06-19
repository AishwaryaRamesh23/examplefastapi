"""add user table

Revision ID: 5b36725aeaaf
Revises: 3bad4522255b
Create Date: 2024-06-11 12:03:02.898379

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '5b36725aeaaf' # revision identifiers, used by Alembic.
down_revision: Union[str, None] = '3bad4522255b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass

def downgrade():
    op.drop_table('users')
    pass
