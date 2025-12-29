from sqlalchemy import ForeignKey, TIMESTAMP, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .database import Base


class Category(Base):
    __tablename__= "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # Foreign key
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    # Relationship
    owner: Mapped["User"] = relationship(back_populates="categories")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

    __table_args__ = (
        UniqueConstraint("name", "owner_id", name="unique_category_per_user")
    )

class Expense(Base):
    __tablename__= "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[int] = mapped_column(nullable= False)
    description: Mapped[str | None] = mapped_column()
    date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('now()'))

    # Foreign key
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))

    # Relationship
    owner: Mapped["User"] = relationship(back_populates="expenses")
    category: Mapped["Category"] = relationship(back_populates="expenses")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))


    # The ForeignKey ALWAYS lives on the "Many" side (the Child), never on the "One" side (the Parent).
    # So no ForeignKey needed incase of categories, as the user is the parent here.

    # Relationship
    categories: Mapped[list["Category"]] = relationship(back_populates="owner")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="owner")