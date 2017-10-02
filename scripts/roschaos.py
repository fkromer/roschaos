#!/usr/bin/env python
import rosnode
import rosgraph
import sys
import argparse

# lots of things 'borrowed' from rosnode

try:
    from xmlrpc.client import ServerProxy
except ImportError:
    from xmlrpclib import ServerProxy

parser = argparse.ArgumentParser()
parser.add_argument('ROS_MASTER_URI', type=str, nargs='?', metavar='URI', help='ROS master URI to use.')
args = parser.parse_args()

ID = '/rosnode'
master = rosgraph.Master(ID, master_uri=args.ROS_MASTER_URI)
print ("Using master at {}".format(master.getUri()))

nodes = rosnode.get_node_names()
print ("Known nodes: " + ', '.join(nodes))

for node in nodes:
    print ("  " + node)

    node_api = rosnode.get_api_uri(master, node)
    if not node_api:
        print("    API URI: error (unknown node: {}?)".format(node))
        continue
    print ("    API URI: " + node_api)

    node = ServerProxy(node_api)
    pid = rosnode._succeed(node.getPid(ID))
    print ("    PID    : {}".format(pid))
