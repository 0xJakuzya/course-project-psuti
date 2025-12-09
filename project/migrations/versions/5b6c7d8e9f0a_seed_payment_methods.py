"""Seed payment methods

Revision ID: 5b6c7d8e9f0a
Revises: 4a5b6c7d8e9f
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b6c7d8e9f0a'
down_revision = '4a5b6c7d8e9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert payment methods
    payment_methods_table = sa.table(
        'payment_methods',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String)
    )
    
    op.bulk_insert(
        payment_methods_table,
        [
            {'id': 1, 'name': 'Наличные'},
            {'id': 2, 'name': 'Карта'},
            {'id': 3, 'name': 'Онлайн'},
        ]
    )


def downgrade() -> None:
    # Delete payment methods
    op.execute("DELETE FROM payment_methods WHERE id IN (1, 2, 3)")

