ARG R_VERSION=4.2.2

FROM rocker/r-ver:${R_VERSION}

SHELL [ "/bin/bash", "-e", "-u", "-x", "-o", "pipefail", "-c"]

# Fix issues with rpy2 not finding shared R libraries
# https://github.com/rpy2/rpy2/issues/675#issuecomment-612289736
RUN echo ${R_HOME}/lib > /etc/ld.so.conf.d/Rlib.conf && ldconfig

ARG PYTHON_VERSION=3.10.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    cmake \
    zlib1g-dev \
    pandoc \
    libicu-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    curl \
    python3="${PYTHON_VERSION}-*" \
    python3-dev="${PYTHON_VERSION}-*" \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"

ARG POETRY_VERSION=1.4.0

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /app

RUN install2.r --error --skipinstalled --ncpu -1 --deps TRUE \
    SPOT \
    && rm -rf /tmp/downloaded_packages \
    && strip /usr/local/lib/R/site-library/*/libs/*.so

COPY poetry.lock pyproject.toml README.md ./
COPY sgm_kriging_models/ ./sgm_kriging_models/
COPY test/ ./test/

RUN poetry config virtualenvs.in-project true \
    && poetry install

RUN poetry run python -m unittest

CMD ["poetry", "run", "uvicorn", "sgm_kriging_models.main:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080
