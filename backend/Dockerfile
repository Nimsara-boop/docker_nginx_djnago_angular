FROM python:3.13-slim AS builder
RUN mkdir app
WORKDIR /app
COPY requirements.txt ./
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app .