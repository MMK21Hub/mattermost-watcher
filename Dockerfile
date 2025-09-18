FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app

# Copy project files
COPY . .
RUN uv sync --locked

EXPOSE 9060
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["python", "main.py"]
