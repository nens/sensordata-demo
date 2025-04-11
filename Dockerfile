FROM python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Whether debugging mode is enabled. Default is set to False
ENV DEBUG=False

# Installation of the app.
WORKDIR /code
COPY pyproject.toml uv.lock ./
RUN uv sync
ENV PATH="/code/.venv/bin:$PATH"

COPY . .
RUN uv sync

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://localhost:8000/ || exit 1
