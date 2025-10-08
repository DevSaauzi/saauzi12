# Stage 1: Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=saauzi.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (uncomment in production)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "saauzi.wsgi:application"]