# Dockerfile for Smithery deployment
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
RUN pip install uv

# Copy all files
COPY . .

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the LIVE server with real Sei data
CMD ["uv", "run", "mcp-agents/mcp/server/analyze_server_live_http.py"]
