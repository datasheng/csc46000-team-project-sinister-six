# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the app code
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# Run the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]