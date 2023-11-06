FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt ./code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./code/requirements.txt

COPY ./backend/ /app/backend
COPY ./data ./app/data

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "80"]
