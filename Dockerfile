# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Force cache invalidation (for testing)
RUN echo "Forcing cache invalidation at $(date)"

# Show contents of requirements.txt
RUN echo "📦 Current requirements.txt:" && cat requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port your app runs on
EXPOSE 8080

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Start the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

