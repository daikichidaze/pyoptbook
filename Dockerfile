FROM python:3
USER root

RUN apt-get update

ARG project_dir=/workdir
WORKDIR $project_dir

ADD requirements.txt $project_dir

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt