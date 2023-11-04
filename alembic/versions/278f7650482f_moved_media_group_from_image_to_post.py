"""Moved media group from image to post

Revision ID: 278f7650482f
Revises: ca01506184b5
Create Date: 2023-11-04 02:32:22.398760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '278f7650482f'
down_revision: Union[str, None] = 'ca01506184b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photo', 'media_group_id')
    op.add_column('post', sa.Column('media_group_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'media_group_id')
    op.add_column('photo', sa.Column('media_group_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###