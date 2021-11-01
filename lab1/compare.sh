#!/bin/bash

for i in */ ; do
do
	echo "Testing $i"
	#python3 LeksickiAnalizator.py < $i/test.in | diff $i/test.out -
done

