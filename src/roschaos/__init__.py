#!/usr/bin/env python
# Software License Agreement (Apache License 2.0)
#
# Copyright 2017 Florian Kromer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from __future__ import print_function
import rosnode
import rosgraph
import rospy
import sys
import os
import signal
import argparse
import socket
import time

try:
    from xmlrpc.client import ServerProxy
except ImportError:
    from xmlrpclib import ServerProxy

NAME='roschaos'
ID = '/roschaos'

class ROSChaosException(Exception):
    """
    Base exception class of roschaos-related errors
    """
    pass

class ROSChaosMonkey(object):
    """
    ROSChaosMonkey creates chaos in ROS nodes randomly.
    """
    def __init__(self, ros_master_uri):
        self.ros_master_uri = ros_master_uri
        self.master = None
        self._discover_ros_master()
        self.discover_ros_nodes()
        self.node_names = None

    def discover_ros_nodes(self):
        self.node_names = rosnode.get_node_names()
        print ("Known nodes: " + ', '.join(self.node_names))
        for node in self.node_names:
            print ("  " + node)
            node_api = rosnode.get_api_uri(self.master, node)
            if not node_api:
                print("    API URI: error (unknown node: {}?)".format(node))
                continue
            print ("    API URI: " + node_api)
            node = ServerProxy(node_api)
            pid = rosnode._succeed(node.getPid(ID))
            print ("    PID    : {}".format(pid))

    def kill_local_node_process(self, pid):
        os.kill(pid, signal.SIGTERM)

    def _discover_ros_master(self):
        self.master = rosgraph.Master(ID, master_uri=self.ros_master_uri)
        print ("Using master at {}".format(self.master.getUri()))

def roschaos_main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('ROS_MASTER_URI', type=str, nargs='?', metavar='URI', help='ROS master URI to use (default: local ROS master URI).\nE.g. ./roschaos http://e330:11311')
    args = parser.parse_args()

    try:
        rcm = ROSChaosMonkey(args.ROS_MASTER_URI)
    except socket.error:
        sys.stderr.write("Network communication failed. Most likely failed to communicate with master.\n")
        sys.exit(1)
    except rosgraph.MasterException as e:
        # mainly for invalid master URI/rosgraph.masterapi
        sys.stderr.write("ERROR: %s\n"%str(e))
        sys.exit(1)
    except KeyboardInterrupt: pass
    except rospy.ROSInterruptException: pass

    # time.sleep(2)
    # rcm.kill_local_node_process(8908)  # an actual pid of e.g. the listener
    # rcm.discover_ros_nodes()
