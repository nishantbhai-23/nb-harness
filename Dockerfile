FROM python:3.12-slim

# Install git and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . .

# Install uv and project dependencies
RUN pip install --no-cache-dir uv && \
    uv sync

CMD ["uv", "run", "python", "-m", "ant_harness"]
