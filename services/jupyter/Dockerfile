FROM jupyter/minimal-notebook

WORKDIR /home/$NB_USER/work

COPY ./data ./data
COPY pyproject.toml ./

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev