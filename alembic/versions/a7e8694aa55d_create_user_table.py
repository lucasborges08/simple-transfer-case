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
        sa.Column('password_salt', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade():
    op.drop_table('users')



# INSERT INTO users values('82a66624-6582-4080-83d2-b4ca067e3a0f', 'nome aleatório', 'email@email.com.br', '84346762069', 500, false, 'asdfsfdohasofh', '24121313', now(), now());

# INSERT INTO users values('2b975081-75a0-4247-b91d-97ec0460db68', 'outro nome aleatório', 'email2@email.com.br', '72336576023', 500, false, 'asdfsfdohasofh', '24121313', now(), now());

# def data_upgrades():
#     """Add any optional data upgrade migrations here!"""
#
#     my_table = table('users',
#                      column('id', UUID),
#                      column('name', sa.String),
#                      column('email', sa.String),
#                      column('doc_number', sa.String),
#                      column('balance', sa.Float),
#                      column('is_storekeeper', sa.Boolean),
#                      column('password', sa.String),
#                      column('password_salt', sa.String),
#                      column('created_at', sa.DateTime),
#                      column('updated_at', sa.DateTime)
#                      )
#
#     op.bulk_insert(my_table,
#         [
#             {'id': UUID('82a66624-6582-4080-83d2-b4ca067e3a0f'), 'name': 'nome aleatório', 'email': 'email@email.com.br',
#              'doc_number': '84346762069', 'balance': 500, 'is_storekeeper': False, 'password': 'asdfsfdohasofh',
#              'password_salt': '24121313', 'created_at': datetime.now(), 'updated_at': datetime.now()},
#
#             {'id': UUID('2b975081-75a0-4247-b91d-97ec0460db68'), 'name': 'outro nome aleatório',
#              'email': 'email2@email.com.br', 'doc_number': '84346762069', 'balance': 500, 'is_storekeeper': False,
#              'password': 'asdfsfdohasofh', 'password_salt': '24121313', 'created_at': datetime.now(),
#              'updated_at': datetime.now()}
#         ]
#     )
