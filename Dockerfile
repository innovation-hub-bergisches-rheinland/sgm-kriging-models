ARG R_VERSION=4.2.2

FROM r-base:${R_VERSION}

SHELL [ "/bin/bash", "-e", "-u", "-x", "-o", "pipefail", "-c"]

ARG PYTHON_VERSION=3.11.2

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    cmake \
    libcurl4-openssl-dev \
    libssl-dev \
    curl \
    python3=${PYTHON_VERSION}-* \
    python3-dev=${PYTHON_VERSION}-* \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"

ARG POETRY_VERSION=1.3.2

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

COPY requirements.R ./

RUN Rscript requirements.R

COPY poetry.lock pyproject.toml README.md ./
COPY sgm_kriging_models/ ./sgm_kriging_models/
COPY test/ ./test/

RUN poetry config virtualenvs.in-project true \
    && poetry install

# RUN poetry run python -m unittest

# CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
