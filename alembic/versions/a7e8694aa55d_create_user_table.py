"""create user table

Revision ID: a7e8694aa55d
Revises: 
Create Date: 2021-08-11 22:44:47.291942

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import table, column
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'a7e8694aa55d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('email', sa.String(150), nullable=False, unique=True),
        sa.Column('doc_number', sa.String(30), nullable=False, unique=True),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('is_storekeeper', sa.Boolean(), nullable=False),
        sa.Column('password', sa.String(500), nullable=False),
        sa.Column('password_salt', sa.String(35), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():
    op.drop_table('users')
