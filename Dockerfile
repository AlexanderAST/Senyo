FROM python:3.13-alpine

RUN apk update && \
    apk add --no-cache gcc musl-dev postgresql-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6565

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "6565"]