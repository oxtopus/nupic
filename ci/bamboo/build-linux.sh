#!/bin/bash
set -o errexit
set -o xtrace
apt-get update
apt-get install -y \
    curl \
    wget \
    git-core \
    gcc \
    g++ \
    cmake \
    python \
    python2.7 \
    python2.7-dev \
    zlib1g-dev \
    bzip2 \
    libyaml-dev \
    libyaml-0-2
wget https://bootstrap.pypa.io/get-pip.py -O - | python
pip install --upgrade setuptools
pip install wheel
export CC=gcc
export CXX=g++
pip install nupic.bindings-0.3.2.dev0-cp27-cp27mu-linux_x86_64.whl
