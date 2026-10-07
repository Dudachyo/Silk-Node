
from sqlalchemy import ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class Person(Base):
    __tablename__ = "persons"
    id : Mapped[int] = mapped_column(primary_key=True)
    owner_user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    note: Mapped[str | None] = mapped_column(default=None)
    is_self : Mapped[bool] = mapped_column(default=False)
    is_favourite : Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        Index(
            "uq_person_self_per_owner",
            "owner_user_id",
            unique=True,
            postgresql_where=text("is_self IS TRUE"),
        ),
    )
