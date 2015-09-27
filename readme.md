# a parallel processing framework for R

Pretty easy setup here:  edit rsetup.R with additional packages. Add components to the dockerfile to install apt-get files as needed. When done, back out the the root of the repo and run docker-compose build . rdockerhpc
(you can name this whatever you want)


to run: 
```{bash}
$ docker-compose up -d slave
$ docker-compose run master
```

to scale (replace n with desired number of nodes): 

```{bash}
$ docker-compose scale slave=n
```

So, to create 2 additional slave nodes: 

```{bash}
docker-compose scale slave=2
```


# test scenario (single host)

Let's say you have a host with a bunch of cpus (or even a few). Preferably this would be a linux machine. If it is not, you may be better off using just the redis server:

```{bash}
$ docker-compose up -d redis
```

Then, as a toy example, you can do something like this:
```{r}
require(doRedis)
host=system('docker-machine ip default',intern=T)
registerDoRedis(host=host,queue='jobs',nodelay=F)
foreach(i=1:100)%dopar%{runif(1)}
startLocalWorkers(host=host,nodelay=F,n=4,queue='jobs')
```
This code chunk imports the doRedis package, gets the local host ip (which we need to get in a weird way if running on os x. If we were doing this on a linux machine or something that ran docker natively, we would just use 'localhost'). Then it registers the redis server and queues up 100 jobs to draw a random number. The last line comissions the worker processes (distributed across cores).

## do it all in docker

You could also do this locally through docker and with compose. This is handy
because you have greater control over the worker processes -- you can start and
stop individual ones etc.

From bash:

```{bash}
# start one worker process. will start redis if not running
$ docker-compose up -d slave 
# launch into the master node with R:
$ docker-compose run master 
```
At this point you will be in R and you can run:
```{r}
foreach(i=1:100)%dopar%{runif(1)}
```

To scale, and add new processes, go back to bash and:
```{bash}
docker-compose scale slave=6
```

This will kill or launch worker containers as needed to get to 6 total. Because
we are using redis for job listing, we don't necessarily loose  if we cancel one
of the worker processes, and we can bring in new ones as desired. Note the
number of workers should be no more than the number of cores. We get some real
leverage with this if we are running on a 32 core machine or something like
that. You would want to tweak the docker compose file to allow containers to take full advantage of processor speeds and ram allotments. 
 

# kubernetes (in testing)

If we have multiple machines and we want to distribute computing across them, we can still use docker and redis but things get complicated. The primary reason for this is that docker is not yet natively set up to accommodate the type of distributed computing we want or need. A container launched will be scheduled to colocate with its linked containers. This leaves 2 options -- do some truly janky networking hacks -- which sort of defeats the point of using docker, or, use a meta container setup like fleet, mesos, or amazon's proprietary system (ECS) to treat a distributed set of nodes as a singular *logical* system. I'm trying this out with kubernetes




Get up and running quickly with the following. It will setup kubernetes and spinup using vagrant. Vagrant is messy here, though, so the dns will break if you kill the vagrant vms (i.e `vagrant destroy` or `vagrant kill`).  A simple restart will fix and this shouldn't be a problem when moving to cloud platforms.)

```{bash}
$ export KUBERNETES_PROVIDER=vagrant
$ export NUM_MINIONS=2
$ curl -sS https://get.k8s.io | bash
```
This will take some time (and bandwith -- go get coffee)

Spin up test environment: This runs from root of the repo

```{bash}
# setup the redis process
$ ./kubernetes/cluster/kubectl.sh create -f ./kube-setup/redis.yaml 

# make it a service so that it's accessable for discovery via dns -- traffic to 'redis' will route to the redis pod 
$ ./kubernetes/cluster/kubectl.sh create -f ./kube-setup/redis_service.yaml 

# provision our worker process
$ ./kubernetes/cluster/kubectl.sh create -f ./kube-setup/rslave.yml 
```

At the moment, I'm still working out the best way to expose the interface to user input. Because cloud computing is expensive, it's probably worth setting this up to take in a script, but alternatives might include using the rstudio docker image here, instead of the bare r-base image I use here.


```{bash}
# provision our worker process
$ ./kubernetes/cluster/kubectl.sh create -f ./kube-setup/rmaster.yml 
# start the master in a stupid way:
$ ./kubernetes/cluster/kubectl.sh exec -it rmaster -- bash
```


Alternatively, you could setup a script to do run the appropriate r commands:


```{bash}
$ ./kubernetes/cluster/kubectl.sh exec rmaster -- Rscript -e \
"require(doRedis);registerDoRedis(host='redis',queue='jobs');foreach(i=i:100)%dopar% runif(1)"
```

