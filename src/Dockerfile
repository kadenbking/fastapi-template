# Use the official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install the Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the necessary port
EXPOSE 80

# Run the server
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "80"]