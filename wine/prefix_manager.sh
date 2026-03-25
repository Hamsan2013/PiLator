#!/bin/bash

PREFIX=~/PiLator/wineprefix

if [ ! -d "$PREFIX" ]; then

echo "Creating Wine prefix..."

WINEPREFIX=$PREFIX wineboot

fi

echo "Wine prefix ready"
