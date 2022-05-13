FROM python:3.9.12-slim
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/code
WORKDIR $APP_HOME

ENV DOCKERIZE_VERSION v0.6.1
RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ADD src/app/requirements.txt $APP_HOME/
RUN pip install -r requirements.txt

COPY . $APP_HOME
CMD flask run --host=0.0.0.0