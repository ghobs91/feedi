"""user kindle credentials

Revision ID: f52cbbaeab22
Revises: 2ab46a53ab1b
Create Date: 2023-10-23 13:04:05.303609

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f52cbbaeab22'
down_revision: Union[str, None] = '2ab46a53ab1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('kindle_devices',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('credentials', sa.VARCHAR(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('user_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kindle_devices')
    # ### end Alembic commands ###