#!/usr/bin/env python

import roschaos
import os

# backup PATH: echo $PATH > path_bkp.txt
# setup - https://github.com/pexpect/pexpect/blob/master/tests/test_pxssh.py
orig_path = os.environ.get('PATH')
fakessh_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fakessh'))
os.environ['PATH'] = fakessh_dir + ((os.pathsep + orig_path) if orig_path else '')
ros_master_uri = os.environ['ROS_MASTER_URI']
rcm = roschaos.ROSChaosMonkey(ros_master_uri, host='server', username='me', password='s3cret')

# execution
rcm.discover_remote_nodes()

# teardown
if orig_path:
    os.environ['PATH'] = orig_path
else:
    del os.environ['PATH']

print(rcm.remote_nodes)
