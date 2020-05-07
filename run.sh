#!/bin/bash

myscript(){
    python3 restropressprint.py
}

until myscript; do
    echo "'Restropress Printer' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
