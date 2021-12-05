#!/bin/bash

if uname -o | grep -q "Msys"; then
	python3="py"
else
	python3="python3"
fi

for i in test/*/ ;
do
	echo "Testing $i"
	
	if $python3 LeksickiAnalizator.py < $i/test.in | diff --strip-trailing-cr $i/test.out -; then
		echo "OK"
	elif [[ $* == *--stop* ]]; then
		break
	fi
done

