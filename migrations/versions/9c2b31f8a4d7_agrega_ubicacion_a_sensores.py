"""agrega ubicación a sensores

Revision ID: 9c2b31f8a4d7
Revises: 41665aba7dee
Create Date: 2026-08-21

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c2b31f8a4d7"
down_revision: str | Sequence[str] | None = "41665aba7dee"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Agrega una ubicación obligatoria preservando sensores existentes."""
    op.add_column(
        "sensors",
        sa.Column("location", sa.String(length=150), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE sensors SET location = name WHERE location IS NULL"
        )
    )

    with op.batch_alter_table("sensors") as batch_op:
        batch_op.alter_column(
            "location",
            existing_type=sa.String(length=150),
            nullable=False,
        )


def downgrade() -> None:
    """Elimina la ubicación de los sensores."""
    with op.batch_alter_table("sensors") as batch_op:
        batch_op.drop_column("location")
