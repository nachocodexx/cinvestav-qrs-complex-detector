FROM python:3.8.6-slim-buster

WORKDIR /app

COPY ./requirements.txt .

RUN pip install pybind11
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y \
    gcc \
    build-essential \
    zlib1g-dev \
    wget \
    unzip \
    cmake \
    python3-dev \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    && apt-get clean

RUN pip install numpy
RUN pip install scipy
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ .


CMD ["python","main.py"]