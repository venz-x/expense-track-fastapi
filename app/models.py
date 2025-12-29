from sqlalchemy import ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .database import Base


class Category(Base):
    __tablename__= "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)

    # owner_id: Mapped[int] = 
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

class Expense(Base):
    __tablename__= "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[int] = mapped_column(nullable= False)
    description: Mapped[str | None] = mapped_column()
    date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(back_populates="expenses")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))