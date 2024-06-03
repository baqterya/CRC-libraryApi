FROM python:3.12.2-slim
LABEL authors="Jakub Jedros"

ARG app_port
ARG app_name
ARG postgres_user
ARG postgres_password
ARG postgres_db
ARG postgres_port

ENV APP_PORT=$app_port
ENV APP_NAME=$app_name
ENV POSTGRES_USER=$postgres_user
ENV POSTGRES_PASSWORD=$postgres_password
ENV POSTGRES_DB=$postgres_db
ENV POSTGRES_PORT=$postgres_port

WORKDIR /libraryapi
COPY ./requirements.txt /libraryapi/requirements.txt
RUN pip install --no-cache-dir -r /libraryapi/requirements.txt
COPY . /libraryapi

#CMD ["python", "/libraryapi/app/main.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]