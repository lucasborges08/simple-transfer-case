"""create transfers table

Revision ID: 32a07cc09570
Revises: a7e8694aa55d
Create Date: 2021-08-12 18:46:09.727734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '32a07cc09570'
down_revision = 'a7e8694aa55d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transfers',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('from_user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('to_user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():
    op.drop_table('transfers')
