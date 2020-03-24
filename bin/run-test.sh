#!/usr/bin/env bash

BIN_DIR=`dirname $0`
ROOT_DIR=`dirname $BIN_DIR`

cd $ROOT_DIR
ROOT_DIR=`pwd`
BIN_DIR=$ROOT_DIR/bin
SRC_DIR=$ROOT_DIR/src
TEST_DIR=$ROOT_DIR/test

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
elif [[ ! -d $TEST_DIR ]]
then
    echo "$TEST_DIR is not directory!"
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

TEST_POST_DATA=$TEST_DIR/_test_post_data
DEFAULT_FNAME=$TEST_DIR/_default
PROG_PATH=$SRC_DIR/client.py

POST_DATA=$(find test/postdata -type f -name '*.pst' 2>/dev/null | tr ' ' '\n' | sort)

DATETIMES=(`date +%s`)

for datafile in $POST_DATA
do
    source $datafile
    source $DEFAULT_FNAME

    RECEIVED=$(eval $PROG_PATH $ADDRESS POST $DATA)

    if [[ "$POST_EXPECTED" != "$RECEIVED" ]]
    then
        echo "$datafile - FAIL"
        echo -e "POST $datafile FAILED"\
                "\POST_EXPECTED (${#POST_EXPECTED} symbols):\n$POST_EXPECTED"\
                "\nRECEIVED (${#RECEIVED} symbols):\n$RECEIVED"
        exit 1
    fi

    DATETIMES+=(`date +%s`)
    sleep 1

    echo "$datafile - POST"
done

echo ${DATETIMES[*]}

TESTS=$(find test/testcases -type f -name '*.tst' 2>/dev/null | tr ' ' '\n' | sort)

for test in $TESTS
do
    source $DEFAULT_FNAME
    source $test

    EXPECTED=$OUT
    RECEIVED=`eval "$PROG_PATH $ADDRESS $METHOD $ARGS"`

    if [[ "$EXPECTED" != "$RECEIVED" ]]
    then
        echo "$test - FAIL"
        echo -e "TEST $test FAILED"\
                "\nEXPECTED (${#EXPECTED} symbols):\n$EXPECTED"\
                "\nRECEIVED (${#RECEIVED} symbols):\n$RECEIVED"
        exit 1
    fi

    echo "$test - OK"
done
