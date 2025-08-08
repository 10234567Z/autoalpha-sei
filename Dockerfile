# Dockerfile for containerized deployment
FROM python:3.13-slim

WORKDIR /app

# Install uv for faster package management
RUN pip install uv

# Copy requirements
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY mcp-agents/mcp/server/analyze_server_simple_http.py ./
COPY mcp-agents/mcp/server/analyze_server.py ./

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the server
CMD ["uv", "run", "analyze_server_simple_http.py"]
