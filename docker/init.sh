/usr/sbin/nginx
nohup /usr/bin/mysqld &

sleep 3

export PYTHONPATH=/metis

sed -i 's/127.0.0.1/9.9.9.9/g' /metis/uweb/dist/app.js
sed -i 's/127.0.0.1/9.9.9.9/g' /metis/uweb/dist/_sample_sampleinfo.js

sleep 3

nohup python /metis/app/controller/manage.py runserver 0.0.0.0:38324 &
/bin/sh
