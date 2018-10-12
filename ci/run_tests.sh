#!/usr/bin/env bash
# Run tests

# echo path
echo $DIR, `pwd`
echo "hello world"

py.test -x -vv -s `pwd`/tests/
sh `pwd`/ci/init_mysql_data.sh