# migrations/versions/0001_initial.py
"""Initial migration

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'workflows',
        sa.Column('workflow_id', sa.Integer, primary_key=True),
        sa.Column('workflow_name', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('status', sa.String, default="paused"),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('created_by', sa.Integer),
        sa.Column('dsl_file', sa.Text)
    )

def downgrade():
    op.drop_table('workflows')
