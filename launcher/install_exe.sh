#!/bin/bash

APP=$1

APPNAME=$(basename "$APP" .exe)

mkdir -p ~/PiLator/apps/$APPNAME

cp "$APP" ~/PiLator/apps/$APPNAME/

echo "$APPNAME installed in PiLator"
