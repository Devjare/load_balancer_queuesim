#!/bin/bash

# ./single $INTERARRIVAL $SERIVCETIME $NUM_DELAY > output/queue_output
# printenv > output/envs
mkdir -p output/T${TEST_NO}
echo "REPORT WORKER ${WORKER}" >> output/T${TEST_NO}/queue_output.workers
echo "single ${INTERARRIVAL} ${SERVICETIME} ${NUM_DELAY}" >> output/T${TEST_NO}/queue_output.workers
./single ${INTERARRIVAL} ${SERVICETIME} ${NUM_DELAY} >> output/T${TEST_NO}/queue_output.workers
