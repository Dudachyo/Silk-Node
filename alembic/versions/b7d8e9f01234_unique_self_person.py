"""Allow at most one self person per user.

Revision ID: b7d8e9f01234
Revises: 4ac0e16a88a6
"""
from alembic import op
import sqlalchemy as sa

revision = "b7d8e9f01234"
down_revision = "4ac0e16a88a6"
branch_labels = None
depends_on = None


def upgrade():
    # Existing duplicates must be resolved explicitly; do not change user data.
    op.create_index(
        "uq_person_self_per_owner",
        "persons",
        ["owner_user_id"],
        unique=True,
        postgresql_where=sa.text("is_self IS TRUE"),
    )


def downgrade():
    op.drop_index("uq_person_self_per_owner", table_name="persons")
