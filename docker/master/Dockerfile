FROM r-base

RUN apt-get -y update && apt-get -y install libxml2-dev
RUN apt-get -y install libssl-dev
RUN apt-get -y install libcurl4-openssl-dev

RUN mkdir /rsetup

ADD ./rsetup.R /rsetup/rsetup.R
RUN Rscript /rsetup/rsetup.R

ADD ./Rprofile_master /root/.Rprofile
CMD R --no-save




