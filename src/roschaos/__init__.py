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

from __future__ import print_function
import rosnode
import rosgraph
import rospy
import sys
import os
import signal
import argparse
import socket
import time
import random
import logging

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

    def discover_ros_nodes(self):
        self.nodes = {}
        node_names = rosnode.get_node_names()
        logging.info("Known nodes: " + ', '.join(node_names))
        for node_name in node_names:
            logging.info("   " + node_name)
            node_api = rosnode.get_api_uri(self.master, node_name)
            if not node_api:
                sys.stderr.write("    API URI: error (unknown node: %s)"%str(node_name))
                continue
            logging.info("    API URI: " + node_api)
            node = ServerProxy(node_api)
            pid = rosnode._succeed(node.getPid(ID))
            logging.info("    PID    : " + str(pid))
            self.nodes[node_name] = {}
            self.nodes[node_name]['uri'] = node_api
            self.nodes[node_name]['pid'] = pid

    def kill_local_node_process_randomly(self):
        node_name = random.choice(self.nodes.keys())
        print("Local node killed: {}".format(node_name))
        self.kill_local_node_process(self.nodes[node_name]['pid'])

    def kill_local_node_process(self, pid):
        os.kill(pid, signal.SIGTERM)

    def _discover_ros_master(self):
        self.master = rosgraph.Master(ID, master_uri=self.ros_master_uri)
        logging.info("Master uri: " + self.master.getUri())

def roschaos_main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', help="Simulate command, don't execute it.",
                        action='store_true')
    parser.add_argument('--version', action='version', version="%(prog)s 0.0.1")
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase output verbosity.")
    parser.add_argument('ROS_MASTER_URI', type=str, nargs='?', metavar='uri',
        help='ROS master URI to use (default: local ROS master URI).\n\
            E.g. ./roschaos http://e330:11311')
    parser.add_argument('-mintd', '--minimal_time_delay', type=int, default=0,
        help='Min. time delay relative to script start in seconds after which \
            chaos is created (default: no lower bound limitation).')
    parser.add_argument('-maxtd', '--maximal_time_delay', type=int, default=sys.maxint,
        help='Max. time delay relative to script start in seconds after which \
            chaos is created (default: no upper bound limitation).')
    args = parser.parse_args()

    if args.dry_run:
        args.verbose = True

    chaos_delay = random.randint(args.minimal_time_delay, args.maximal_time_delay)

    if args.verbose > 0:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    elif args.verbose > 1:
        logging.basicConfig(format='%(message)s', level=logging.WARNING)

    if args.verbose > 0:
        if args.dry_run:
            print("Dry run, actual command would execute with the following config:")
    logging.info("minimal time delay in seconds: " + str(args.minimal_time_delay))
    logging.info("maximal time delay in seconds: " + str(args.maximal_time_delay))
    logging.info("actual chaos time delay in seconds: " + str(chaos_delay))

    if args.dry_run:
        sys.exit(0)
    else:
        try:
            rcm = ROSChaosMonkey(args.ROS_MASTER_URI)
        except socket.error:
            sys.stderr.write("Network communication failed. Most likely failed to \
                communicate with master.\n")
            sys.exit(1)
        except rosgraph.MasterException as e:
            # mainly for invalid master URI/rosgraph.masterapi
            sys.stderr.write("ERROR: %s\n"%str(e))
            sys.exit(1)
        except KeyboardInterrupt: pass
        except rospy.ROSInterruptException: pass

        print("Delay until kill: {}".format(chaos_delay))
        time.sleep(chaos_delay)
        rcm.kill_local_node_process_randomly()
        sys.exit(0)
