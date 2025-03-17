# Dockerfile

# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY StackOverFlow_Crawler_Kafka/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY StackOverFlow_Crawler_Kafka/ .

# Set the command to run the application
CMD ["python", "main.py"]