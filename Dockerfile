ARG R_VERSION=4.2.2

FROM r-base:${R_VERSION}

SHELL [ "/bin/bash", "-e", "-u", "-x", "-o", "pipefail", "-c"]

ARG PYTHON_VERSION=3.11.2

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    cmake \
    zlib1g-dev \
    pandoc \
    libicu-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    curl \
    python3=${PYTHON_VERSION}-* \
    python3-dev=${PYTHON_VERSION}-* \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"

ARG POETRY_VERSION=1.4.0

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

RUN install2.r --error --skipinstalled --ncpu -1 --deps TRUE \
    SPOT \
    && rm -rf /tmp/downloaded_packages

COPY poetry.lock pyproject.toml README.md ./
COPY sgm_kriging_models/ ./sgm_kriging_models/
COPY test/ ./test/

RUN poetry config virtualenvs.in-project true \
    && poetry install

RUN poetry run python -m unittest

CMD ["poetry", "run", "uvicorn", "sgm_kriging_models.main:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080
