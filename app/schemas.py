from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import List

# =======================
# 1. BASE MODELS 
# (Shared fields only. NO passwords)
# =======================
class CategoryBase(BaseModel):
    name: str

class ExpenseBase(BaseModel):
    amount: int
    description: str | None = None
    date: datetime | None = None

class UserBase(BaseModel):
    email: EmailStr

class BudgetBase(BaseModel):
    amount: int

class BudgetStatusBase(BaseModel):
    category: str
    amount: int
    spend: int
    remaining: int
    status: str

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

class BudgetCreate(BudgetBase):
    pass

# =======================
# 3. RESPONSE MODELS (OUTPUT)
# (IDs, dates, but NO passwords)
# =======================
class Expense(ExpenseBase):
    id: int
    category_id: int
    owner_id: int

    date: datetime

    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CategoryBreakdown(BaseModel):
    category_name: str
    total_amount: int

class Budget(BudgetBase):
    id: int
    owner_id: int
    category_id: int
    category_name: str

    model_config = ConfigDict(from_attributes=True)

class BudgetStatus(BudgetStatusBase):
    
    model_config = ConfigDict(from_attributes=True)

# =======================
# 4. Updating
# =======================
class CategoryUpdate(BaseModel):
    name: str | None = None

class ExpenseUpdate(BaseModel):
    amount: int | None = None
    description: str | None = None
    date: datetime | None = None

class BudgetUpdate(BudgetBase):
    pass

# =======================
# 5. RELATIONSHIP MODELS
# =======================
class ExpenseWithCategory(Expense):
    category: Category

class CategoryWithExpenses(Category):
    expenses: List[Expense] = []