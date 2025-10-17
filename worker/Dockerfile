# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
# We go up one directory (..) to find the requirements.txt
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the worker script into the container
COPY worker.py .

# Run worker.py when the container launches
CMD ["python", "worker.py"]