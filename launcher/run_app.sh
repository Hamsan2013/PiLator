#!/bin/bash

APP=$1

echo "Launching $APP"

box86 wine "$APP"
