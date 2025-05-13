# Use a slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY generate_data.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "generate_data.py"]
