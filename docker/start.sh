if [ $# == 0 ]
then
	echo "Need at least 1 argument!"
	exit
fi
ip=$1
sed -i "s/9.9.9.9/${ip}/g" init.sh
docker build -t local/metis-demo:1.0 .
docker run -i -t -p80:80 -p8080:8080 local/metis-demo:1.0
