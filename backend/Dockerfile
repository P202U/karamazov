FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY ./app ./app

EXPOSE 8000

RUN useradd -m karamazov_user
USER karamazov_user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]