"""empty message

Revision ID: c412a89cbb80
Revises: 582628f02a84
Create Date: 2024-04-14 16:33:08.333276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c412a89cbb80'
down_revision: Union[str, None] = '582628f02a84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('SNL', sa.String(), nullable=True),
    sa.Column('data_birth', sa.Integer(), nullable=True),
    sa.Column('date_death', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('history', sa.String(), nullable=True),
    sa.Column('main_photo', sa.String(), nullable=True),
    sa.Column('photo', sa.VARCHAR(), nullable=True),
    sa.Column('medals', sa.String(), nullable=True),
    sa.Column('date_pulished', sa.Integer(), nullable=True),
    sa.Column('rank', sa.String(), nullable=True),
    sa.Column('role', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('persons')
    # ### end Alembic commands ###
