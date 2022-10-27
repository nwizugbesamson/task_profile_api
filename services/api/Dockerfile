# builder #
FROM python:3.10.6-slim as builder

# set work directory
WORKDIR /usr/src/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc


# requirements file
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/api/wheels -r requirements.txt


# FINAL #

# pull official base image
FROM python:3.10.6-slim-buster

# virtual environment
RUN python3 -m venv /opt/venv

# create directory for the app user
RUN mkdir -p /home/api

# create the app user
RUN addgroup --system api && adduser --system --group api




# create the appropriate directories

ENV HOME=/home/api
ENV APP_HOME=/home/api/web
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/api/wheels /wheels
COPY --from=builder /usr/src/api/requirements.txt .
RUN pip install --upgrade pip && pip cache purge
RUN pip install --no-cache /wheels/*




# copy all files into docker directory app
COPY . .
ENV PATH="./entrypoint.sh:$PATH"

# chown all the files to the app user
RUN chmod +x ./entrypoint.sh  &&\
    chown -R api:api $APP_HOME



# change to the app user
USER api

# run entrypoint.prod.sh
# ENTRYPOINT ["/home/api/web/entrypoint.sh"]




