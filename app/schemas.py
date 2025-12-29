from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import List, Optional

# =======================
# 1. BASE MODELS 
# (Shared fields only. NO passwords)
# =======================
class CategoryBase(BaseModel):
    name: str

class ExpenseBase(BaseModel):
    amount: int
    description: str
    date: datetime

class UserBase(BaseModel):
    email: EmailStr

# =======================
# 2. CREATE MODELS (INPUT)
# (passwords/secrets)
# =======================
class CategoryCreate(CategoryBase):
    pass

class ExpenseCreate(ExpenseBase):
    category_id: int

class UserCreate(UserBase):
    password: str

class LoginBase(BaseModel):
    email: EmailStr
    password: str

# =======================
# 3. RESPONSE MODELS (OUTPUT)
# (IDs, dates, but NO passwords)
# =======================
class Expense(ExpenseBase):
    id: int
    category_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# =======================
# 4. RELATIONSHIP MODELS
# =======================
class ExpenseWithCategory(Expense):
    category: Category

class CategoryWithExpenses(Category):
    expenses: List[Expense]