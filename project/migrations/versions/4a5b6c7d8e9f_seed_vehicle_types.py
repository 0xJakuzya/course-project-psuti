"""Seed vehicle types

Revision ID: 4a5b6c7d8e9f
Revises: 3d4649c4556b
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a5b6c7d8e9f'
down_revision = '3d4649c4556b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert vehicle types
    vehicle_types_table = sa.table(
        'vehicle_types',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String)
    )
    
    op.bulk_insert(
        vehicle_types_table,
        [
            {'id': 1, 'name': 'Легковой'},
            {'id': 2, 'name': 'Мотоцикл'},
            {'id': 3, 'name': 'Грузовой'},
        ]
    )


def downgrade() -> None:
    # Delete vehicle types
    op.execute("DELETE FROM vehicle_types WHERE id IN (1, 2, 3)")

