from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CategoryBase(BaseModel):
    name: str

class ExpenseBase(BaseModel):
    amount: int
    description: str
    date: datetime

# -------create--------
class CategoryCreate(CategoryBase):
    pass

class ExpenseCreate(ExpenseBase):
    category_id: int

# ---------response--------
class Expense(ExpenseBase):
    id: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# ---------relationship----------
class ExpenseWIthCategory(Expense):
    category: Category

class CategoryWithExpense(Category):
    expense: list[Expense]