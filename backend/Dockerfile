# Use slim Python base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the backend project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn",
