# roschaos
Functionality for process reliability/fault recovery testing in ROS.

## Installation

    cd <catkin-workspace>/src
    git clone https://github.com/fkromer/roschaos.git
    cd ..
    catkin_make --pkg roschaos
    . devel/setup.bash

## Usage

### Script Mode

Start `roscore` and other ROS nodes in separate terminals

    roscore

e.g. using the "builtin" talker

    cd test
    ./talker.py

and listener

    cd test
    ./listener.py

Use `roschaos` in another terminal (consider `roschaos -h` for a full command
  line option list) ...

    roschaos -mintd=1 -maxtd=3

... to kill a random local ROS node

    Delay until kill: 2
    Local node killed: /talker_29276_1507242893110

... which killed the talker process

    (a lot more output)
    [INFO] [1507243233.965743]: hello world 1507243233.97
    [INFO] [1507243234.065729]: hello world 1507243234.07
    [INFO] [1507243234.165768]: hello world 1507243234.17
    (process has been killed)

### Node Mode

The ROS node `chaos` can be used with `rosrun`, `roslaunch` launch files or in
`rostest` tests.

#### Usage in `rosrun`

Start `roscore` and other ROS nodes in separate terminals

    roscore

and execute the `chaos` node in another terminal

    rosrun roschaos chaos _mintd:=1 _maxtd:=3

#### Usage in `roslaunch`

Create a launch file `chaos.launch` with the following content

    <launch>
      <node name="chaos" pkg="roschaos" type="chaos" output="screen">
        <param name="mintd" value="1"/>
        <param name="maxtd" value="3"/>
      </node>
    </launch>

and execute it with `roslaunch chaos.launch`.

### Library Mode

Import the class `roschaos.ROSChaosMonkey` into your Python script/library and
consider `roschaos.roschaos_main` how it can be used.

For a minimal "library mode" example start `roscore` in a terminal and try
`roschaos` in a separate terminal:

    python
    >>> import roschaos
    >>> import os
    >>> rcm = roschaos.ROSChaosMonkey(os.environ['ROS_MASTER_URI'])
    >>> rcm.kill_local_node_process_randomly()
    Local node killed: /rosout

The `/rosout` process has been killed:

    started core service [/rosout]
    [rosout-1] process has died [pid 6237, exit code -15, cmd /opt/ros/kinetic/lib/rosout/rosout __name:=rosout __log:=/home/florian/.ros/log/7000f9d8-ab50-11e7-86a0-6036dd110fcb/rosout-1.log].
    log file: /home/florian/.ros/log/7000f9d8-ab50-11e7-86a0-6036dd110fcb/rosout-1*.log
    [rosout-1] restarting process

## Development

Add `roschaos` to the PYTHONPATH:

    export PYTHONPATH=$PYTHONPATH:~/ws_catkin/src/roschaos/src

Start `roscore`, `talker.py` and `listener.py` in separate terminals:

    roscore

    cd test
    ./talker.py

    cd test
    ./listener.py

Execute `roschaos`:

    cd scripts
    ./roschaos.py
