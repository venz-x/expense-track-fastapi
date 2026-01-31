# Use a lightweight Python version
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (this makes rebuilding faster)
COPY requirements.txt .

# Install dependencies (FastAPI, SQLAlchemy, Pydantic, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]