#!/bin/bash

MODULE_NAME=dlpfs
SLEEP_TIME=5

echo "BENCHMARK FOR LOOPBACK"

python3 -m $MODULE_NAME -r input -m output -t loopback -l ERROR -sub -re2 &

sleep $SLEEP_TIME

echo "READ"

for size in 1 $(seq 5 5 100) $(seq 200 50 500) $(seq 500 500 20000); do
    for i in $(seq 30); do
        echo -n "$size $i "
        { time cat ./output/$size-lines.csv > /dev/null ; } 2>&1 | grep real | tr 'm.s' ' ' | awk '{print ($4 + 1000 * ($3 + 60 * $2))}'
    done
done > results/read-loopback.dat

echo "WRITE"

for size in 1 $(seq 5 5 100) $(seq 200 50 500) $(seq 500 500 20000); do
    for i in $(seq 30); do
        rm  -f input/t$i
        echo -n "$size $i "
        { time cat ./input/$size-lines.csv > ./output/t$i ; } 2>&1 | grep real | tr 'm.s' ' ' | awk '{print ($4 + 1000 * ($3 + 60 * $2))}'
    done
done > results/write-loopback.dat

echo "STOPPING LOOPBACK"

ps aux | grep $MODULE_NAME | grep -v grep | awk '{print $2}' | xargs kill -SIGINT

for rule in $(ls -1 ./benchmark-rules); do

    for guard_size in 2 4 8 16 32 64 128 256; do

        echo "BENCHMARK FOR $MODULE_NAME $rule $guard_size"

        python3 -m $MODULE_NAME -r input -m output -t $MODULE_NAME -s benchmark-rules/$rule -l ERROR -sub -re2 -g $guard_size &

        sleep $SLEEP_TIME

        echo "READ"

        for size in 1 $(seq 5 5 100) $(seq 200 50 500) $(seq 500 500 20000); do
            for i in $(seq 30); do
                echo -n "$size $i "
                { time cat ./output/$size-lines.csv > /dev/null ; } 2>&1 | grep real | tr 'm.s' ' ' | awk '{print ($4 + 1000 * ($3 + 60 * $2))}'
            done
        done > results/read-$rule-$guard_size.dat

        echo "WRITE"

        for size in 1 $(seq 5 5 100) $(seq 200 50 500) $(seq 500 500 20000); do
            for i in $(seq 30); do
                echo -n "$size $i "
                { time cat ./input/$size-lines.csv > ./output/t$i ; } 2>&1 | grep real | tr 'm.s' ' ' | awk '{print ($4 + 1000 * ($3 + 60 * $2))}'
            done
        done > results/write-$rule.dat

        echo "STOPPING $MODULE_NAME $rule $guard_size"

        ps aux | grep $MODULE_NAME | grep -v grep | awk '{print $2}' | xargs kill -SIGINT
    done
done
