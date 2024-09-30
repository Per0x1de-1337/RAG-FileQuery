# Use the official Python image from Docker Hub
FROM python:latest

# Set a working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000 9000

# Command to run the Flask app
CMD ["python", "server.py"]
