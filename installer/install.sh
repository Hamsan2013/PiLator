#!/bin/bash

echo "Installing PiLator v2..."

sudo apt update

echo "Installing dependencies..."

sudo apt install git build-essential cmake python3 python3-tk wine -y

echo "Installing Box86..."

cd ~

git clone https://github.com/ptitSeb/box86

cd box86
mkdir build
cd build

cmake .. -DRPI3=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo

make -j4

sudo make install

echo "Creating PiLator directories..."

mkdir -p ~/PiLator/apps
mkdir -p ~/PiLator/wineprefix

echo "PiLator installed successfully!"
