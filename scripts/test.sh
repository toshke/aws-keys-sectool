#!/bin/bash

cmd="python3 setup.py install && aws-keys-sectool list-keys"

versions="3.6 3.7 3.8 3.9 3.10"
set -x
for v in $versions; do
    echo "Testing install and list with version $x"
    docker run --rm -it \
        -v $PWD:/src \
        -w /src \
        -v $HOME/.aws:/root/.aws "python:${v}-alpine"  /bin/sh -c "$cmd"
done