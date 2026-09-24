FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin

WORKDIR /code
ENV PATH "/code/.venv/bin:$PATH"

# 1. Copy configuration files AND the README.md
COPY pyproject.toml .python-version uv.lock README.md ./

# 2. Copy the source directory 
COPY src/ ./src/

# 3. Synchronize environments
RUN uv sync --locked
COPY pipeline.py .

# 4. Use the virtual environment's python to run your script
ENTRYPOINT ["python", "pipeline.py"]
