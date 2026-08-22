"""add user role

Revision ID: df6eb308da81
Revises: 742065fa3490
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df6eb308da81"
down_revision: Union[str, Sequence[str], None] = "742065fa3490"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add role column to users."""

    user_role = sa.Enum(
        "USER",
        "ADMIN",
        name="user_role",
    )

    user_role.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="USER",
        ),
    )

    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Remove role column from users."""

    op.drop_column("users", "role")

    user_role = sa.Enum(
        "USER",
        "ADMIN",
        name="user_role",
    )

    user_role.drop(op.get_bind(), checkfirst=True)
