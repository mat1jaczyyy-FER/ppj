#!/bin/bash

for i in test/*/ ;
do
	echo "Testing $i"
	python3 LeksickiAnalizator.py < $i/test.in | diff --strip-trailing-cr $i/test.out -
done

