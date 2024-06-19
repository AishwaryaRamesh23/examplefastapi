"""add foreign-key to posts table

Revision ID: e1ba580ad63d
Revises: 5b36725aeaaf
Create Date: 2024-06-11 15:34:46.900325

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'e1ba580ad63d'  # revision identifiers, used by Alembic.
down_revision: Union[str, None] = '5b36725aeaaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('smposts',sa.Column('user_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="smposts",referent_table="users",local_cols=['user_id'],remote_cols=['id'],ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('posts_users_fk',table_name="smposts")
    op.drop_column('posts','user_id')
    pass
