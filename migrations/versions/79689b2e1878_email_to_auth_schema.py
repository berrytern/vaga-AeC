"""email_to_auth_schema

Revision ID: 79689b2e1878
Revises: de0f78533d1c
Create Date: 2024-12-16 17:07:21.567068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "79689b2e1878"
down_revision: Union[str, None] = "de0f78533d1c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    admin_emails = connection.execute(
        sa.text("SELECT id, email FROM admin WHERE email IS NOT NULL")
    ).fetchall()

    reader_emails = connection.execute(
        sa.text("SELECT id, email FROM reader WHERE email IS NOT NULL")
    ).fetchall()

    op.add_column("auth", sa.Column("email", sa.String(), nullable=True))

    for admin_id, email in admin_emails:
        connection.execute(
            sa.text("UPDATE auth SET email = :email WHERE foreign_id = :id"),
            {"email": email, "id": admin_id},
        )

    for reader_id, email in reader_emails:
        connection.execute(
            sa.text("UPDATE auth SET email = :email WHERE foreign_id = :id"),
            {"email": email, "id": reader_id},
        )
    op.create_unique_constraint(None, "auth", ["email"])

    op.drop_constraint("admin_email_key", "admin", type_="unique")
    op.drop_column("admin", "email")

    op.drop_constraint("reader_email_key", "reader", type_="unique")
    op.drop_column("reader", "email")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()

    auth_emails = connection.execute(
        sa.text("SELECT email, user_type, foreign_id FROM auth WHERE email IS NOT NULL")
    ).fetchall()
    op.add_column(
        "reader", sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.create_unique_constraint("reader_email_key", "reader", ["email"])

    op.add_column(
        "admin", sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.create_unique_constraint("admin_email_key", "admin", ["email"])

    for email, user_type, foreign_id in auth_emails:
        connection.execute(
            sa.text(f"UPDATE {user_type} SET email = :email WHERE id = :id"),
            {"email": email, "id": foreign_id},
        )

    op.drop_constraint(None, "auth", type_="unique")
    op.drop_column("auth", "email")

    # ### end Alembic commands ###