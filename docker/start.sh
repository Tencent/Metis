#!/bin/bash
if [ $# == 0 ]
then
        echo "Usage:$0 <IP Address>"
        exit 1
fi
ip=$1

docker rm -f metis-db
docker rm -f metis-svr
docker rm -f metis-web

docker run --net=host --name=metis-db -d -p 3306:3306 -v /data/metis/mysql/:/var/lib/mysql:Z -e MYSQL_ROOT_PASSWORD=metis@123 zhiyunmetis/metis-db
sleep 6
docker run --net=host --name=metis-svr -d -p 8080:8080 -v /data/metis/model/:/metis/time_series_detector/model:Z zhiyunmetis/metis-svr /bin/sh /metis/init.sh
docker run --net=host --name=metis-web -d -p 80:80 zhiyunmetis/metis-web /bin/sh /metis/init.sh ${ip}
