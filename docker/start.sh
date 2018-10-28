if [ $# == 0 ]
then
        echo "Need at least 1 argument!"
        exit
fi
ip=$1

docker rm -f metis-db
docker rm -f metis-svr
docker rm -f metis-web

docker run --net=host --name=metis-db -i -t -d -p 3306:3306 -v /data/metis/mysql/:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=metis@123 zhiyunmetis/metis-db
sleep 6
docker run --net=host --name=metis-svr -i -t -d -p 8080:8080 -v /data/metis/module/:/metis/app/model/time_series_detector zhiyunmetis/metis-svr /bin/sh /metis/init.sh
docker run --net=host --name=metis-web -i -t -d -p 80:80 zhiyunmetis/metis-web /bin/sh /metis/init.sh ${ip}
