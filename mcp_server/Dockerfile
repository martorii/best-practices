FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY . .

# Synchronize dependencies
RUN uv sync --frozen

EXPOSE 8000

# Use 'uv run' to ensure the environment is used
CMD ["uv", "run", "server.py"]
