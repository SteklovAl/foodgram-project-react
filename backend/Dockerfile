FROM python:3.7-slim

WORKDIR /app

COPY backend/requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./backend/ /app

CMD ["gunicorn", "foodgram_project.wsgi:application", "--bind", "0:8000" ]