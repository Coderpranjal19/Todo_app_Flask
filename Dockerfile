# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Initialize the SQLite database
RUN python -c "from app import db; db.create_all()"

# Specify the command to run the application
CMD ["python", "app.py"]
