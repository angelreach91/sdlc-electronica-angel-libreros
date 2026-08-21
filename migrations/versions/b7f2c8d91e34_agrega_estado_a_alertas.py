"""agrega estado a alertas

Revision ID: b7f2c8d91e34
Revises: 9c2b31f8a4d7
Create Date: 2026-08-21

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7f2c8d91e34"
down_revision: str | Sequence[str] | None = "9c2b31f8a4d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Agrega un estado obligatorio preservando alertas existentes."""

    op.add_column(
        "alerts",
        sa.Column("status", sa.String(length=20), nullable=True),
    )
    op.execute(
        sa.text("UPDATE alerts SET status = 'open' WHERE status IS NULL")
    )

    with op.batch_alter_table("alerts") as batch_op:
        batch_op.alter_column(
            "status",
            existing_type=sa.String(length=20),
            nullable=False,
        )


def downgrade() -> None:
    """Elimina únicamente el estado de las alertas."""

    with op.batch_alter_table("alerts") as batch_op:
        batch_op.drop_column("status")
