# Build stage
FROM python:3.12.2-bullseye as buildstage

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y -q && \
    apt-get install -y -q --no-install-recommends \
      python3-dev

RUN python3 -m pip install --upgrade pip setuptools wheel

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt


# Main stage
FROM python:3.12.2-bullseye as mainstage

LABEL maintainer="muhammadfikri6844@gmail.com"
LABEL org.label-schema.schema-version="1.0"
ARG BUILD_DATE
LABEL org.label-schema.build-date=$BUILD_DATE
ARG BUILD_VERSION
LABEL org.label-schema.version=$BUILD_VERSION


COPY --from=buildstage /opt/venv /opt/venv

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"
ENV DATABASE_URL="postgresql://bluesheets:bluesheets@postgresql:5432/sys?schema=public"

RUN ["mkdir", "-p", "/opt/docker/app/src"]
WORKDIR /opt/docker/app

COPY ./src ./src
COPY ./startup.sh ./startup.sh

RUN ["mkdir", "-p", "/opt/docker/logs"]
VOLUME ["/opt/docker/logs"]

EXPOSE 8888

CMD ["./startup.sh"]