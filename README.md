# roschaos
Functionality for process reliability/fault recovery testing in ROS.

## Installation

    cd <catkin-workspace>
    git clone https://github.com/fkromer/roschaos.git
    catkin_make --pkg roschaos
    . devel/setup.bash

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
