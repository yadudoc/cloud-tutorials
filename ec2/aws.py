#!/usr/bin/env python

import os
import configurator
import sys
import random
import logging

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeSize, NodeImage
from libcloud.compute.types import NodeState
import libcloud.compute.types

NODESTATES = { NodeState.RUNNING    : "RUNNING",
               NodeState.REBOOTING  : "REBOOTING",
               NodeState.TERMINATED : "TERMINATED",
               NodeState.STOPPED    : "STOPPED",
               NodeState.PENDING    : "PENDING",
               NodeState.UNKNOWN    : "UNKNOWN" }

logging.basicConfig(filename='aws.log', level=logging.INFO)

def list_resources(driver):

    resources = driver.list_nodes()
    if not resources:
        print "No active resources"
    else:
        print '-'*51
        print '{0:20} | {1:10} | {2:15}'.format("NAME", "STATUS", "EXTERNAL_IP")
        print '-'*51
        for resource in resources:
            if resource.public_ips:
                #print resource.name, " | ", NODESTATES[resource.state] , " | ", resource.public_ips[0]
                print '{0:20} | {1:10} | {2:15}'.format(resource.name, NODESTATES[resource.state], resource.public_ips[0])
                print '-'*51

    return resources


def get_public_ip(driver, name):
    resources = driver.list_nodes()
    if not resources:
        print "No active resources"
    for resource in resources:
        if resource.name == name and resource.public_ips:
            print resource.public_ips[0]
            return resource

    print "Could not find a resource with the id ", name
    return -1

def aws_create_security_group(driver, configs):
    group_name = configs["SECURITY_GROUP"]
    current    = driver.ex_list_security_groups()
    if group_name in current:
        logging.info("Security group: %s is already present", group_name)
    else:
        logging.info("Creating new security group: %s", group_name)
        res = driver.ex_create_security_group(name=group_name,description="Open all ports")
        if not driver.ex_authorize_security_group(group_name, 0, 65000, '0.0.0.0/0'):
            logging.info("Authorizing ports for security group failed")
        if not driver.ex_authorize_security_group(group_name, 0, 65000, '0.0.0.0/0', protocol='udp'):
            logging.info("Authorizing ports for security group failed")
        logging.debug("Security group: %s", str(res))

def check_keypair(driver, configs):
    if "AWS_KEYPAIR_NAME" in configs and "AWS_KEYPAIR_FILE" in configs:
        logging.debug("AWS_KEYPAIR_NAME : %s", configs['AWS_KEYPAIR_NAME'])
        logging.debug("AWS_KEYPAIR_FILE : %s", configs['AWS_KEYPAIR_FILE'])
        all_pairs = driver.list_key_pairs()
        for pair in all_pairs:
            if pair.name == configs['AWS_KEYPAIR_NAME']:
                logging.info("KEYPAIR exists, registered")
                return 0

        logging.info("KEYPAIR does not exist. Creating keypair")
        key_pair = driver.create_key_pair(name=configs['AWS_KEYPAIR_NAME'])
        f = open(configs['AWS_KEYPAIR_FILE'], 'w')
        f.write(str(key_pair.private_key))
        f.close()
        os.chmod(configs['AWS_KEYPAIR_FILE'], 0600)
        logging.info("KEYPAIR created")
    else:
        logging.error("AWS_KEYPAIR_NAME and/or AWS_KEYPAIR_FILE missing")
        logging.error("Cannot proceed without AWS_KEYPAIR_NAME and AWS_KEYPAIR_FILE")
        exit(-1)


def start_headnode(driver, configs):
    userdata   = configurator.getstring("headnode")

    # Check if headnode
    nodes      = driver.list_nodes()
    headnode   = False
    for node in nodes:
        if node.name == "headnode" and node.state == NodeState.RUNNING:
            headnode = node
            print "INFO: Headnode is RUNNING"
            return 0

    sizes      = driver.list_sizes()
    size       = [ s for s in sizes if s.id == configs['HEADNODE_MACHINE_TYPE'] ][0]
    image      = NodeImage(id=configs['HEADNODE_IMAGE'], name=None, driver=driver)
    node       = driver.create_node(name='headnode',
                                    image=image,
                                    size=size,
                                    ex_keyname=configs['AWS_KEYPAIR_NAME'],
                                    ex_securitygroup=configs['SECURITY_GROUP'],
                                    ex_userdata=userdata )
    print "INFO: Waiting for headnode bootup ..."
    driver._wait_until_running(node, wait_period=5, timeout=240)
    print "INFO: Headnode active!"
    if node.public_ips:
        print '-'*51
        print '{0:20} | {1:10} | {2:15}'.format(node.name, NODESTATES[node.state], node.public_ips[0])
        print '-'*51
        f = open('./PUBLIC_ADDRESS', 'w')
        f.write(str(node.public_ips[0]))
        f.close()



def start_worker(driver, configs, worker_names):
    nodes       = driver.list_nodes()
    headnode    = False
    disk_info   = False
    volume      = False
    disk_info   = ""
    concurrency = "-c 1" # Default concurrency for workers
    init_string = ""

    for node in nodes:
        if node.name == "headnode" and node.state == NodeState.RUNNING:
            headnode = node
    if not headnode :
        print "WARNING : No active headnode found"
        return -1

    # Setup userdata
    userdata   = configurator.getstring("worker")
    userdata   = userdata.replace("SET_HEADNODE_IP", headnode.public_ips[0])

    # Setting worker concurrency level
    if 'WORKER_CONCURRENCY' in configs:
        concurrency = "-c " + str(configs['WORKER_CONCURRENCY'])
    userdata    = userdata.replace("SET_CONCURRENCY", concurrency)

    # Inserting WORKER_INIT_SCRIPT
    if 'WORKER_INIT_SCRIPT' in configs :
        if not os.path.isfile(configs['WORKER_INIT_SCRIPT']):
            print "Unable to read WORKER_INIT_SCRIPT"
            exit(-1);
        init_string = open(configs['WORKER_INIT_SCRIPT'], 'r').read()
    userdata    = userdata.replace("#WORKER_INIT_SCRIPT", init_string)

    if 'WORKER_DISK' in configs:
        disk_info  = configs['WORKER_DISK'].split(" ")
        location   = driver.list_locations()[0];
        volume     = driver.create_volume(size=500, location=location, name="test volume 500gb")
    else:
        print "No worker_disk defined"

    logging.info("Worker userdata : %s", userdata)
    list_nodes = []
    sizes      = driver.list_sizes()
    size       = [ s for s in sizes if s.id == configs['WORKER_MACHINE_TYPE'] ]
    if not size:
        logging.info("ec2workerimage not legal/valid : %s", configs['WORKER_MACHINE_TYPE'])
        sys.stderr.write("WORKER_MACHINE_TYPE not legal/valid \n")
        exit(-1);

    image      = NodeImage(id=configs['WORKER_IMAGE'], name=None, driver=driver)
    print size

    for worker_name in worker_names:
        node       = driver.create_node(name=worker_name,
                                        image=image,
                                        size=size[0],
                                        ex_keyname=configs['AWS_KEYPAIR_NAME'],
                                        ex_securitygroup=configs['SECURITY_GROUP'],
                                        #block_device_mapping=mapping,
                                        ex_userdata=userdata )
        if volume:
            driver.attach_volume(node, volume, device=disk_info[1] )

        list_nodes.append(node)
        logging.info("Worker node started : %s",str(node))


def terminate_all_nodes():
    configs,driver = init()
    nodes          = driver.list_nodes()
    for node in nodes:
        print "Deleting node : ", node.name
        driver.destroy_node(node)

# node_names is a list
def terminate_node(driver, node_names):
    nodes          = driver.list_nodes()
    deleted_flag   = False
    for node in nodes:
        if node.name in node_names and node.state == NodeState.RUNNING :
            print "Deleting node : ", node.name
            code = driver.destroy_node(node)
            deleted_flag = True
    return deleted_flag


def init():
    configs    = configurator.read_configs('configs')
    #configurator.pretty_configs(configs)
    driver     = get_driver(Provider.EC2_US_WEST_OREGON) # was EC2
    ec2_driver = driver(configs['AWSAccessKeyId'], configs['AWSSecretKey'])
    aws_create_security_group(ec2_driver, configs)
    check_keypair(ec2_driver, configs)
    return configs,ec2_driver

def help():
    help_string = """ Usage for aws.py : python aws.py [<option> <arguments...>]
    start_worker <worker_id>*: Starts worker with name set to worker_id, returns a unique id
    stop_node <id>*          : Terminates the node which matches the id with its name or unique id
    start_headnode           : Starts the headnode, to which workers connect to
    stop_headnode            : Terminates the headnode
    dissolve                 : Terminates all active resources
    list_resources           : List all resources
    list_resource <id/name>  : List the public ip and state of the resource
"""
    print help_string
    exit(1)

# Main driver section
configs, driver = init()
args = sys.argv[1:]

if len(args) < 1:
    help()

if   args[0] == "start_worker":
    worker_name = ["swift-worker-" + str(random.randint(1,999))]
    if len(args) >=  2 :
        worker_name = args[1:]
    start_worker(driver,configs,worker_name)

elif args[0] == "start_headnode":
    start_headnode(driver,configs)

elif args[0] == "stop_headnode":
    terminate_node(driver,["headnode"])

elif args[0] == "stop_node":
    if len(args) >=  2 :
        worker_names = args[1:]
        terminate_node(driver,worker_names)
    else:
        help()

elif args[0] == "dissolve":
    terminate_all_nodes()

elif args[0] == "list_resources":
    list_resources(driver)

elif args[0] == "list_resource":
    if len(args) !=  2 :
        help
    get_public_ip(driver, args[1])

else:
    print "ERROR: Option ", args[0], " not recognized"
    help()
