# --- Builder stage ---
FROM python:3.14-slim AS builder

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir .

# --- Production stage ---
FROM python:3.14-slim

RUN useradd --create-home --shell /bin/bash botuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY src/ src/

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER botuser

CMD ["python", "-m", "src.main"]
