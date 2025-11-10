from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass

class CustomerDB(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column (primary_key = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[str] = mapped_column(String, index = True, unique = True, nullable = False)
    customer_since: Mapped[int] = mapped_column(Integer, nullable = False)
    order_number: Mapped[int] = mapped_column(Integer, unique = True, nullable = False)
    total_cents: Mapped[int] = mapped_column(Integer, nullable = False)
    orders: Mapped[list["OrderDB"]] = relationship(back_populates = "owner", cascade = "all, delete-orphan")


class OrderDB(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column (primary_key = True)
    description: Mapped[str] = mapped_column(String, nullable = False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("customer_id", ondelete = "CASCADE"), nullable = False)
