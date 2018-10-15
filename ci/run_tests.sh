#!/usr/bin/env bash
# Run tests

echo $DIR, `pwd`

py.test -x -vv -s `pwd`/tests/
#sh `pwd`/ci/init_mysql_data.sh
