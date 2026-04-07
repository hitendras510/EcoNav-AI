# Use a specific slim Python image that matches openenv.yaml
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860

# Set working directory
WORKDIR /app

# Install system dependencies
# Install system dependencies with better error handling and common tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Copy ONLY requirements first to leverage Docker cache
COPY requirements/ ./requirements/
COPY pyproject.toml uv.lock ./

# Install project dependencies with uv
RUN uv pip install --system --no-cache -r requirements/backend.txt -r requirements/ml.txt

# Copy the rest of the application
COPY . .

# Set up a new user named "user" with UID 1000 for HF Spaces compatibility
RUN useradd -m -u 1000 user && \
    chown -R user:user /app
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Expose the standard Hugging Face Space port
EXPOSE 7860

# No HEALTHCHECK needed for standard HF Spaces and validator deployments,
# simplifies build logic and reduces potential for false failures.

# Start the application using uvicorn correctly
CMD ["uvicorn", "apps.backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
