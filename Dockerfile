FROM python:3.7-alpine

RUN apk add --update py-pip
RUN apk --no-cache add poetry

RUN poetry config virtualenvs.create false

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml /app
COPY README.md /app 

RUN mkdir /app/run_across_america
COPY run_across_america /app/run_across_america

# App uses a CLI, so we need to run install last
RUN poetry install --no-dev

ENTRYPOINT [ "runaa-cli" ]