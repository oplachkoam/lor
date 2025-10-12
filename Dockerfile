FROM python:3.13-alpine

RUN apk add --no-cache build-base curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /server

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY ./migrations ./migrations
COPY ./src ./src

EXPOSE 8000

ENV PYTHONPATH=/server

CMD ["uv", "run", "python", "src/main.py"]
