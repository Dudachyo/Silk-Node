

from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class Connection(Base):
    __tablename__ = "connections"
    id : Mapped[int] = mapped_column(primary_key=True)
    owner_user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_a_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person_b_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    via: Mapped[str]

    __table_args__ = (
            CheckConstraint(
                "person_a_id < person_b_id",
                name="ck_connection_ordered_pair",
            ),
            UniqueConstraint(
                "owner_user_id",
                "person_a_id",
                "person_b_id",
                name="uq_connection_pair_per_owner",
            ),
        )
