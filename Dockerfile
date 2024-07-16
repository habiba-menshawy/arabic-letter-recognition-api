# Use an appropriate base image
FROM python:3.12-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
