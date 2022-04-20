#!/bin/bash

echo "\nQUEUE OUTPUT: \n"
cp /var/lib/docker/volumes/shared/_data/*.results ./results

export FILES_R=$(ls results | grep -G _R_)
export FILES_RR=$(ls results | grep -G _RR_)
export FILES_TC=$(ls results | grep -G _TC_)

echo "==================================================="
echo "RANDOM RESULTS"
for f in $FILES_R
do
  echo "Results ${f}"
  cat ./results/${f}
done


echo "==================================================="
echo "ROUND ROBING RESULTS"
for f in $FILES_RR
do
  echo "Results ${f}"
  cat ./results/${f}
done

echo "==================================================="
echo "TWO CHOICES RESULTS"
for f in $FILES_TC
do
  echo "Results ${f}"
  cat ./results/${f}
done


