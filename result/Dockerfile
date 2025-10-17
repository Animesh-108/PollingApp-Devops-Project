# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file from the current directory
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the result app script into the container
COPY app.py .

# ADD THIS LINE: Copy the templates directory
COPY templates ./templates

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]