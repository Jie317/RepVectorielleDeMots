#!/bin/bash
echo ">>>>>>>>>begin"
rm -rf build bin
mkdir build


# build and compile
./configure
make

echo "<<<<<<<<<<finished"
