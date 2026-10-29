# syntax=docker/dockerfile:1
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --uid 10001 --no-create-home app
COPY src/ ./src/
COPY static/ ./static/
USER 10001
EXPOSE 5000
ENTRYPOINT ["python", "-m", "src.server"]
