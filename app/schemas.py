from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class CategoryBase(BaseModel):
    name: str

class ExpenseBase(BaseModel):
    amount: int
    description: str
    date: datetime

class LoginBase(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    email: EmailStr
    password: str

# -------create--------
class CategoryCreate(CategoryBase):
    pass

class ExpenseCreate(ExpenseBase):
    category_id: int

class UserCreate(UserBase):
    pass

# ---------response--------
class Expense(ExpenseBase):
    id: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int

# ---------relationship----------
class ExpenseWIthCategory(Expense):
    category: Category

class CategoryWithExpense(Category):
    expense: list[Expense]