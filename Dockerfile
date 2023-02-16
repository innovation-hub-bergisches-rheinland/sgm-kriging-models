FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    r-base \
    python3.10 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    r-base-dev \
    libcurl4-gnutls-dev \
    libxml2-dev \
    libssl-dev \
    cmake

# install r packages
COPY requirements/requirements.R ./configurations/requirements.R
RUN Rscript ./configurations/requirements.R

# standard python libs
COPY requirements/requirements.txt ./configurations/requirements.txt
RUN pip install -r ./configurations/requirements.txt

COPY ./src/ /code/src/
ENV PYTHONPATH="${PYTHONPATH}:/"

WORKDIR /code/
# envs
# ENV INFLUX_HOST='influxdb.dashboard-model-factory'
# ENV INFLUX_PORT=8086

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]