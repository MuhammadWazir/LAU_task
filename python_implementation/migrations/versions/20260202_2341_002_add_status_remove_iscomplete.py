"""add status remove iscomplete

Revision ID: 002
Revises: 001
Create Date: 2026-02-02 23:41:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create status enum
    op.execute("CREATE TYPE task_status AS ENUM ('OPEN', 'DONE');")
    
    # Add status column and drop is_complete column
    op.add_column('tasks', sa.Column('status', sa.Enum('OPEN', 'DONE', name='task_status'), nullable=False, server_default='OPEN'))
    op.drop_column('tasks', 'is_complete')


def downgrade() -> None:
    # Drop status column and add is_complete column
    op.drop_column('tasks', 'status')
    op.add_column('tasks', sa.Column('is_complete', sa.Boolean(), nullable=False, server_default=False))
    
    # Drop status enum
    op.execute("DROP TYPE task_status;")