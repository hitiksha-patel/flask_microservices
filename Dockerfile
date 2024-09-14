# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies, including default-mysql-client
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    default-mysql-client \
    && apt-get clean

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory into the container
COPY . .

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
