# roschaos
Functionality for process reliability/fault recovery testing in ROS.

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
