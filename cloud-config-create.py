import os, sys
import subprocess
from subprocess import Popen
from subprocess import PIPE
import ruamel.yaml
import argparse

parser = argparse.ArgumentParser(description='generate cloud-config file for specified cluster size')
parser.add_argument(dest='x', metavar='cluster size', type=int, 
                   help='number of instances to cluster')

def config_create():
    out=parser.parse_args()
    clusterurl='https://discovery.etcd.io/new?size=%s'%out.x
    print clusterurl
    m=Popen(['curl',clusterurl],stdout=PIPE)
    url=str(m.communicate()[0])
    url

    with open("./cloud-config-template.yaml",'rb') as inp:
        x=ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)

    inp.close()

    x['coreos']['etcd2']['discovery']=url

    with open("./cloud-config.yaml",'wb') as code:
        code.write(ruamel.yaml.dump(x, Dumper= ruamel.yaml.RoundTripDumper))

    code.close()

if __name__ == "__main__":
    config_create()