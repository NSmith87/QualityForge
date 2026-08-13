FROM python:3.12-slim

WORKDIR /app
COPY backend /app
RUN python -m pip install --no-cache-dir .

EXPOSE 8000
CMD ["qualityforge", "serve", "--host", "0.0.0.0", "--port", "8000"]
