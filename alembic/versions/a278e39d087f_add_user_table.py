"""add user table

Revision ID: a278e39d087f
Revises: 39d8cb430445
Create Date: 2023-09-06 13:27:04.915061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a278e39d087f'
down_revision: Union[str, None] = '39d8cb430445'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(), nullable=False), 
                    sa.Column('email',sa.String(), nullable=False),
                    sa.Column('password',sa.String(), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.Text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_column('users')
    pass
