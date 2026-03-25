#!/bin/bash

APP=$1

export WINEDEBUG=-all
export BOX86_DYNAREC=1

echo "Starting Game Mode..."

box86 wine "$APP"
