#!/usr/bin/env bash
for i in 300 1000 2000 3000 4000 5000 6000 7000 8000 ; do
cd ${i}K
printf "current directory is: "$PWD'\n'
qha-run
cd ..
done
wait
             
