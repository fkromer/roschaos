#!/usr/bin/env python

import roschaos
import os

###### local nodes ######

# setup
ros_master_uri = os.environ['ROS_MASTER_URI']
rcm = roschaos.ROSChaosMonkey(ros_master_uri)

# execution
rcm.discover_ros_nodes()

# /talker will be something like /talker_8527_1511384376981
assert any('/talker' in node for node in rcm.nodes), "talker not contained in listed nodes"
assert any('/rosout' in node for node in rcm.nodes), "rosout not contained in listed nodes"
