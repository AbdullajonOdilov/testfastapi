"""Initial migration

Revision ID: b2d2f72e015e
Revises: 430eda9fa2bb
Create Date: 2023-07-28 14:44:49.533240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d2f72e015e'
down_revision = '430eda9fa2bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('process', sa.Column('connection', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('process', 'connection')
    # ### end Alembic commands ###