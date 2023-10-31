#!/bin/bash
mitmdump.exe -s mitm.py &
python3 main.py > output.log 2>&1 &