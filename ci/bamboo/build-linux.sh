#!/bin/bash
set -o errexit
set -o xtrace

# Environment defaults
if [ -z "${USER}" ]; then
    USER="docker"
fi
export USER

# Setup compiler
if [ -z "${CC}" ]; then
    CC="gcc"
fi
export CC

if [ "${CC}" = "clang" ]; then
    if [ -z "${CXX}" ]; then
        CXX="clang++"
    fi
    COMPILER_PACKAGES="clang-3.4" # Ubuntu-specific apt package name
else
    if [ -z "${CXX}" ]; then
        CXX="g++"
    fi
    COMPILER_PACKAGES="${CC} ${CXX}" # Ubuntu-specific apt package names
fi
export CXX

# Install OS dependencies, assuming stock ubuntu:latest
apt-get update
apt-get install -y \
    wget \
    cmake \
    python \
    python2.7 \
    python2.7-dev
wget https://bootstrap.pypa.io/get-pip.py -O - | python
pip install --upgrade --ignore-installed setuptools
pip install wheel

# Install artifacts from previous build
pip install nupic.bindings-*-cp27-cp27mu-linux_x86_64.whl

# Build installable python packages
python setup.py bdist bdist_dumb bdist_wheel sdist
