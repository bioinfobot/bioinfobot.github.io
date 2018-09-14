#!/bin/sh

LOG=".log"
if [ -d "$LOG" ]
then
    echo "SKIP: .log directory already exists."
else
    echo "CREATE: .log directory."
    mkdir .log
fi