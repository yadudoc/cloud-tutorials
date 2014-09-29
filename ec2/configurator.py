#!/usr/bin/env python

import os
import pprint

def _read_conf(config_file):
    cfile = open(config_file, 'r').read()
    config = {}
    for line in cfile.split('\n'):

        # Checking if empty line or comment
        if line.startswith('#') or not line :
            continue

        temp = line.split('=')
        config[temp[0]] = temp[1].strip('\r')
    return config

def pretty_configs(configs):
    printer = pprint.PrettyPrinter(indent=4)
    printer.pprint(configs)


def read_configs(config_file):
    config = _read_conf(config_file)

    if 'AWS_CREDENTIALS_FILE' in config :
        config['AWS_CREDENTIALS_FILE'] =  os.path.expanduser(config['AWS_CREDENTIALS_FILE'])
        config['AWS_CREDENTIALS_FILE'] =  os.path.expandvars(config['AWS_CREDENTIALS_FILE'])

        cred_lines    =  open(config['AWS_CREDENTIALS_FILE']).readlines()
        cred_details  =  cred_lines[1].split(',')
        credentials   = { 'AWS_Username'   : cred_details[0],
                          'AWSAccessKeyId' : cred_details[1],
                          'AWSSecretKey'   : cred_details[2] }
        config.update(credentials)
    else:
        print "AWS_CREDENTIALS_FILE , Missing"
        print "ERROR: Cannot proceed without access to AWS_CREDENTIALS_FILE"
        exit(-1)

    if 'AWS_KEYPAIR_FILE' in config:
        config['AWS_KEYPAIR_FILE'] = os.path.expanduser(config['AWS_KEYPAIR_FILE'])
        config['AWS_KEYPAIR_FILE'] = os.path.expandvars(config['AWS_KEYPAIR_FILE'])
    return config

#configs = read_configs("./configs")
#pretty_configs(configs)

#!/usr/bin/env python

HEADNODE_USERDATA_0_95='''#!/bin/bash
WORKERPORT="50005"; SERVICEPORT="50010"
cd /usr/local/bin
wget http://users.rcc.uchicago.edu/~yadunand/jdk-7u51-linux-x64.tar.gz; tar -xzf jdk-7u51-linux-x64.tar.gz;
wget http://swift-lang.org/packages/swift-0.95-RC6.tar.gz;tar -xzf swift-0.95-RC6.tar.gz;
export JAVA=/usr/local/bin/jdk1.7.0_51/bin
export SWIFT=/usr/local/bin/swift-0.95-RC6/bin
export PATH=$JAVA:$SWIFT:$PATH
apt-get update; apt-get install -y build-essential git libfuse-dev libcurl4-openssl-dev libxml2-dev mime-support libtool mdadm
apt-get install -y automake
cd /home/ubuntu;
git clone https://github.com/s3fs-fuse/s3fs-fuse
cd s3fs-fuse/
./autogen.sh
./configure --prefix=/usr
make && make install
mkdir /scratch;
mdadm --create --verbose /dev/md0 --level=stripe --raid-devices=2 /dev/xvdb /dev/xvdc
mkfs.ext4 /dev/md0; mount -t ext4 /dev/md0 /scratch; chmod 777 /scratch
mkdir /s3; chmod 777 /s3;

coaster_loop ()
{
    while :
    do
        coaster-service -p $SERVICEPORT -localport $WORKERPORT -nosec -passive &> /var/log/coaster-service.logs
        sleep 10;
    done
}
coaster_loop &
'''

HEADNODE_USERDATA_TRUNK='''#!/bin/bash
WORKERPORT="50005"; SERVICEPORT="50010"
cd /usr/local/bin
wget http://users.rcc.uchicago.edu/~yadunand/jdk-7u51-linux-x64.tar.gz; tar -xzf jdk-7u51-linux-x64.tar.gz;
#wget http://swift-lang.org/packages/swift-0.95-RC6.tar.gz;tar -xzf swift-0.95-RC6.tar.gz;
wget http://users.rcc.uchicago.edu/~yadunand/swift-trunk.tar.gz; tar -xzf swift-trunk.tar.gz
export JAVA=/usr/local/bin/jdk1.7.0_51/bin
#export SWIFT=/usr/local/bin/swift-0.95-RC6/bin
export SWIFT=/usr/local/bin/swift-trunk/bin
export PATH=$JAVA:$SWIFT:$PATH
apt-get update; apt-get install -y build-essential git libfuse-dev libcurl4-openssl-dev libxml2-dev mime-support libtool mdadm
apt-get install -y automake
cd /home/ubuntu;
git clone https://github.com/yadudoc/cloud-tutorials.git
chmod 777 cloud-tutorials
git clone https://github.com/s3fs-fuse/s3fs-fuse
cd s3fs-fuse/
./autogen.sh
./configure --prefix=/usr
make && make install
mkdir /scratch;
mdadm --create --verbose /dev/md0 --level=stripe --raid-devices=2 /dev/xvdb /dev/xvdc
mkfs.ext4 /dev/md0; mount -t ext4 /dev/md0 /scratch; chmod 777 /scratch
mkdir /s3; chmod 777 /s3;

coaster_loop ()
{
    while :
    do
        coaster-service -p $SERVICEPORT -localport $WORKERPORT -nosec -passive &> /var/log/coaster-service.logs
        sleep 10;
    done
}
coaster_loop &
'''

WORKER_USERDATA_0_95='''#!/bin/bash
#Replace_me
HEADNODE=SET_HEADNODE_IP
WORKERPORT="50005"
#Ping timeout
apt-get update
apt-get install -y build-essential git libfuse-dev libcurl4-openssl-dev libxml2-dev mime-support libtool mdadm
apt-get install -y automake
cd /home/ubuntu
git clone https://github.com/s3fs-fuse/s3fs-fuse
cd s3fs-fuse/
./autogen.sh
./configure --prefix=/usr
make
sudo make install
cd /usr/local/bin
wget http://users.rcc.uchicago.edu/~yadunand/jdk-7u51-linux-x64.tar.gz; tar -xzf jdk-7u51-linux-x64.tar.gz;
wget http://swift-lang.org/packages/swift-0.95-RC6.tar.gz;tar -xzf swift-0.95-RC6.tar.gz;
export JAVA=/usr/local/bin/jdk1.7.0_51/bin
export SWIFT=/usr/local/bin/swift-0.95-RC6/bin
export PATH=$JAVA:$SWIFT:$PATH
mkdir /scratch;
mdadm --create --verbose /dev/md0 --level=stripe --raid-devices=2 /dev/xvdb /dev/xvdc
mkfs.ext4 /dev/md0; mount -t ext4 /dev/md0 /scratch; chmod 777 /scratch
mkdir /s3; chmod 777 /s3;
s3fs -o allow_other,gid=2300 swift-s3-test /s3 -ouse_cache=/scratch,parallel_count=25
PTIMEOUT=4
#Disk_setup
export JAVA=/usr/local/bin/jdk1.7.0_51/bin
export SWIFT=/usr/local/bin/swift-0.95-RC6/bin
export PATH=$JAVA:$SWIFT:$PATH
export ENABLE_WORKER_LOGGING
export WORKER_LOGGING_LEVEL=DEBUG
worker_loop ()
{
    while :
    do
        echo "Pinging HEADNODE on $HEADNODE"
        #runuser -l ec2-user -c "worker.pl http://$HEADNODE:$WORKERPORT 0099 ~/workerlog -w 3600"
        worker.pl http://$HEADNODE:$WORKERPORT 0099 /var/log -w 3600
        sleep 5
    done
}
worker_loop &
'''

WORKER_USERDATA_TRUNK='''#!/bin/bash
#Replace_me
HEADNODE=SET_HEADNODE_IP
CONCURRENCY="SET_CONCURRENCY"
#WORKER_INIT_SCRIPT
WORKERPORT="50005"
#Ping timeout
apt-get update
apt-get install -y build-essential git libfuse-dev libcurl4-openssl-dev libxml2-dev mime-support libtool mdadm
apt-get install -y automake
cd /home/ubuntu
git clone https://github.com/s3fs-fuse/s3fs-fuse
cd s3fs-fuse/
./autogen.sh
./configure --prefix=/usr
make
sudo make install
cd /usr/local/bin
wget http://users.rcc.uchicago.edu/~yadunand/jdk-7u51-linux-x64.tar.gz; tar -xzf jdk-7u51-linux-x64.tar.gz;
wget http://users.rcc.uchicago.edu/~yadunand/swift-trunk.tar.gz; tar -xzf swift-trunk.tar.gz
export JAVA=/usr/local/bin/jdk1.7.0_51/bin
export SWIFT=/usr/local/bin/swift-trunk/bin
export PATH=$JAVA:$SWIFT:$PATH
mkdir /scratch;
mdadm --create --verbose /dev/md0 --level=stripe --raid-devices=2 /dev/xvdb /dev/xvdc
mkfs.ext4 /dev/md0; mount -t ext4 /dev/md0 /scratch; chmod 777 /scratch
mkdir /s3; chmod 777 /s3;
PTIMEOUT=4
#Disk_setup
export JAVA=/usr/local/bin/jdk1.7.0_51/bin
export SWIFT=/usr/local/bin/swift-trunk/bin
export PATH=$JAVA:$SWIFT:$PATH
export ENABLE_WORKER_LOGGING
export WORKER_LOGGING_LEVEL=DEBUG
worker_loop ()
{
    while :
    do
        echo "Connecting to HEADNODE on $HEADNODE"
        worker.pl -w 3600 $CONCURRENCY http://$HEADNODE:$WORKERPORT 0099 /var/log
        sleep 5
    done
}
worker_loop &
'''


def getstring(target):
    if target == "headnode":
        #return HEADNODE_USERDATA_0_95
        return HEADNODE_USERDATA_TRUNK
    elif target == "worker":
        #return WORKER_USERDATA_0_95
        return WORKER_USERDATA_TRUNK
    else:
        return -1

