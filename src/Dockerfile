
FROM python:3.8-buster
LABEL maintainer=ajjunior

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=linux

# Airflow
ARG AIRFLOW_VERSION=2.7.0
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ARG SPARK_VERSION=3.2.1
ARG HADOOP_VERSION=3.2.1
ENV AIRFLOW_GPL_UNIDECODE=yes

# Define en_US.
ENV LANGUAGE=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8
ENV LC_MESSAGES=en_US.UTF-8

COPY requirements.txt /requirements.txt

# Install dependencies
RUN set -ex && \
    buildDeps=' \
    freetds-dev \
    libkrb5-dev \
    libsasl2-dev \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    git \
    ' && \
    apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends $buildDeps && \
    apt-get install -yqq --no-install-recommends \
    freetds-bin \
    build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    curl \
    rsync \
    netcat \
    locales \
    iputils-ping \
    telnet && \
    sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Add the airflow user
RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow

# Install Python dependencies
RUN pip install -U pip setuptools wheel && \
    pip install pytz && \
    pip install pyOpenSSL && \
    pip install ndg-httpsclient && \
    pip install pyasn1

RUN pip install -r /requirements.txt

# Install Airflow and necessary providers
RUN pip install apache-airflow==${AIRFLOW_VERSION}
RUN pip install "apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh]"
RUN pip install apache-airflow-providers-apache-spark
RUN pip install apache-airflow-providers-amazon
RUN pip install apache-airflow-providers-apache-hdfs
RUN pip install redis

# Setup JAVA_HOME 
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
RUN export JAVA_HOME

# SPARK files and variables
ENV SPARK_HOME=/usr/local/spark

# Finished SPARK files and variables

# Begin Hadoop installation
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow/airflow.cfg

RUN chown -R airflow:airflow ${AIRFLOW_HOME}
RUN chmod +x /entrypoint.sh

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
