# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies needed for psycopg2 and pandas
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first, to leverage Docker cache for dependencies
COPY requirements.txt .

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 for the FastAPI app
EXPOSE 5000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "5000"]
