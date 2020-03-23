#!/usr/bin/env bash

if [[ $# -ge 1 ]]
then
    ROOT_DIR=$1
    BIN_DIR=$ROOT_DIR/bin
else
    BIN_DIR=`dirname $0`
    ROOT_DIR=`dirname $BIN_DIR`
fi

cd $ROOT_DIR
ROOT_DIR=`pwd`
BIN_DIR=$ROOT_DIR/bin
SRC_DIR=$ROOT_DIR/src

if [[ ! -d $ROOT_DIR ]]
then
    echo "$ROOT_DIR is not directory!"
    exit 1
elif [[ ! -d $BIN_DIR ]]
then
    echo "$BIN_DIR is not directory!"
    exit 1
elif [[ ! -d $SRC_DIR ]]
then
    echo "$SRC_DIR is not directory!"
    exit 1
fi

PYTHON_VERS=3.7
PYTHON_NAME=python$PYTHON_VERS
PYTHON_BIN=`which $PYTHON_NAME`

if [[ -z $PYTHON_BIN ]]
then
    echo "Python with version \"$PYTHON_VERS\" has bean not found!"
    exit 1
fi

export PYTHONPATH=$PYTHONPATH:$ROOT_DIR
export ROOT_DIR=$ROOT_DIR

exec $PYTHON_BIN "$SRC_DIR/server.py"
