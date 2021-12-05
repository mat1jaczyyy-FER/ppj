#!/bin/bash

if uname -o | grep -q "Msys"; then
	python3="py"
	node="node.exe"
else
	python3="python3"
	node="node"
fi

for i in test/*/ ;
do
	echo "Testing $i"
	
	if $python3 FRISCGenerator.py < $i/test.in > temp.frisc; then
		echo " FRISCGenerator compiled"

		if $node frisc/main.js -s -cpufreq 20000 temp.frisc | diff --strip-trailing-cr $i/test.out -; then
			echo " R6 output OK"
		else
			echo " R6 error"
			if [[ $* == *--stop* ]]; then
				break
			fi
		fi
	else
		echo " FRISCGenerator error"
		if [[ $* == *--stop* ]]; then
			break
		fi
	fi
done

rm -f temp.frisc