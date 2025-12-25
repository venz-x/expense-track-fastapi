from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date as date_type
from .database import Base


class Category(Base):
    __tablename__= "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)

    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

class Expense(Base):
    __tablename__= "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[int] = mapped_column(nullable= False)
    description: Mapped[str | None] = mapped_column()
    date: Mapped[date_type] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(back_populates="expenses")