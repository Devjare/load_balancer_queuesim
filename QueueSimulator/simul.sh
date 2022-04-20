#!/bin/bash

# ./single $INTERARRIVAL $SERIVCETIME $NUM_DELAY > output/queue_output
# printenv > output/envs
# mkdir -p output/T${TEST_NO}
export FILENAME=W${WORKERS}_${BALANCER}_T${TESTNO}

echo "WORKER=${WORKER}" >> output/$FILENAME.results
echo "single ${INTERARRIVAL} ${SERVICETIME} ${NUM_DELAY}" >> output/$FILENAME.results
./single ${INTERARRIVAL} ${SERVICETIME} ${NUM_DELAY} >> output/$FILENAME.results
echo "--------------------------------------------" >> output/$FILENAME.results
