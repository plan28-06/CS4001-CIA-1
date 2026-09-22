# ---- Smart City Traffic Monitoring System ----
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .

# Document the port the app listens on
EXPOSE 5000

# Basic container-level healthcheck
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run as a non-root user for good practice
RUN useradd -m appuser
USER appuser

CMD ["python", "app.py"]