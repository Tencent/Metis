FROM sherlockren/metis-full
WORKDIR /metis
ADD . /metis
EXPOSE 80
EXPOSE 8080

RUN chmod +x /metis/init.sh 

CMD ["/bin/sh","/metis/init.sh"]

