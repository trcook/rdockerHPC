FROM r-base

RUN apt-get -y update && apt-get -y install libxml2-dev
RUN apt-get -y install libssl-dev
RUN apt-get -y install libcurl4-openssl-dev

RUN mkdir /rsetup

ADD ./rsetup.R /rsetup/rsetup.R
RUN Rscript /rsetup/rsetup.R
RUN Rscript -e 'install.packages("doRedis")'
ADD ./Rprofile /root/.Rprofile
CMD Rscript -e "require('doRedis');try(redisWorker(host='redis',queue='jobs'));redisWorker(host='redis',queue='jobs')"





