FROM python:3.7-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml /app
COPY README.md /app 

RUN mkdir /app/run_across_america
COPY run_across_america /app/run_across_america
RUN poetry install --only main

ENTRYPOINT [ "runaa-cli" ]