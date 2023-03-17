[![CI](https://github.com/innovation-hub-bergisches-rheinland/sgm-kriging-models/actions/workflows/ci.yaml/badge.svg?branch=main&event=push)](https://github.com/innovation-hub-bergisches-rheinland/sgm-kriging-models/actions/workflows/ci.yaml) [![Release Charts](https://github.com/innovation-hub-bergisches-rheinland/sgm-kriging-models/actions/workflows/release.yaml/badge.svg?branch=main&event=push)](https://github.com/innovation-hub-bergisches-rheinland/sgm-kriging-models/actions/workflows/release.yaml)
# Local Development

Install pyenv with the pyenv installer, configure your shell (log out and log back in for changes to take effect):

```
# Install pyenv
curl https://pyenv.run | bash
# Configure shell
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init --path)"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
```

For install on macos see: <https://github.com/pyenv/pyenv>

Install and activate Python version specified in .python-version with pyenv:

```
# Install and activate Python version
pyenv install
# If the command fails and you are using an Apple Silicon Mac use instead
arch -arm64 pyenv install
# Check Python version
pyenv version
```

Install R on system, see: <https://cran.r-project.org/>

Create project environment, install dependencies and activate the environment in your shell:

```
# Configure Poetry to create environments in project directories (OPTIONAL)
poetry config virtualenvs.in-project true
# Create project environment
poetry env use $(which python)
# Install dependencies
poetry install
# Activate project environment
poetry shell
```

Create environment variables for connection to influxdb if not running on default path `localhost:8086`:

```bash
export $INFLUX_HOST=<hostname>
export $INFLUX_PORT=<port>
```

Install R dependencies with `Rscript ./requirements/requirements.R` and R-Python dependencies with `pip install -r ./requirements/requirements.txt`

Run application for dev with: `uvicorn src.main:app --reload`

## Sample data

For local development it can be necessary to run a influxdb and have some example data in the database.
InfluxDB have to be run in version 1.8. To run influxdb via docker use the following command: `docker run -p 8086:8086 influxdb:1.8`.

To add data you have to create a database. First attach to docker container with `docker exec -it <containername> /bin/bash` to
run a shell inside container.

Then connect to influxdb via command `influx`.

After that create the database
with name "aggregation" by typing `CREATE DATABASE aggregation`. If the command run successfully there is no message display.
In case of an error it would be shown.
