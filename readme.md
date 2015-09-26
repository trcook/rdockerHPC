# a parallel processing framework for R

Pretty easy setup here:  edit rsetup.R with additional packages. Add components to the dockerfile to install apt-get files as needed. When done, back out the the root of the repo and run docker-compose build . rdockerhpc
(you can name this whatever you want)


to run: 
run docker-compose up -d slave
run docker-compose run master

to scale (replace n with desired number of nodes): 
docker-compose scale slave=n

So, to create 2 additional slave nodes: 
docker-compose scale slave=2
