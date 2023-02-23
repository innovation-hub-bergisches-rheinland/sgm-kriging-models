

FROM python:3.11.2-bullseye as base

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    r-base \
    r-base-dev \
    libcurl4-gnutls-dev \
    libxml2-dev \
    libssl-dev \
    cmake

# install r packages
COPY requirements/requirements.R ./configurations/requirements.R
RUN Rscript ./configurations/requirements.R


# install python packages

FROM base

# standard python libs
COPY requirements/requirements.txt ./configurations/requirements.txt
RUN pip install -r ./configurations/requirements.txt

COPY ./src/ /code/src/
ENV PYTHONPATH="${PYTHONPATH}:/"

WORKDIR /code/

RUN ["python", "-m", "unittest"]


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]