# roschaos
Functionality for process reliability/fault recovery testing in ROS.

## Installation

    cd <catkin-workspace>
    git clone https://github.com/fkromer/roschaos.git
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

### Library Mode

Import the class `roschaos.ROSChaosMonkey` into your Python script/library and
consider `roschaos.roschaos_main` how it can be used.

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
