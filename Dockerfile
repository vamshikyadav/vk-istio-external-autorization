# Use the official Python image as the base image for building
FROM python:3.9-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use a separate stage for the final image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container at /app
COPY authorization_server.py /app/

# Copy installed dependencies from the previous stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Expose the port the server listens on
EXPOSE 8080

# Run the Python script when the container launches
CMD ["python", "authorization_server.py"]
