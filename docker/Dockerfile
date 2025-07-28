# docker/Dockerfile

# --- Build Stage ---
FROM python:3.11-slim-bookworm as builder

WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Set up virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- Final Stage ---
FROM python:3.11-slim-bookworm as final

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /home/appuser/app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser backend/ ./
COPY --chown=appuser:appuser scripts/ ./scripts/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "optionforge:create_app()"]
