FROM python:3.11-slim as base

ARG BRANCH=main

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install git curl
RUN pip install --upgrade pip setuptools

WORKDIR /commons

ARG GIT_TOKEN
RUN git clone -b ${BRANCH} https://${GIT_TOKEN}@github.com/VestimyApp/commons .

RUN pip3 install .

WORKDIR /service

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn

COPY service /service/service

ENV PORT 8080
ENTRYPOINT ["/bin/sh", "-c"]
HEALTHCHECK --interval=1m CMD curl -f http://localhost:${PORT}/health || exit 1
CMD ["uvicorn service.app:app --host 0.0.0.0 --port ${PORT}"]