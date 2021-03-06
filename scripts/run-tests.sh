#!/bin/bash

MODULE_NAME=dlpfs
SLEEP_TIME=10

function kill_process() {
    ps | grep python | awk '{print $1}' | xargs kill
    sleep $SLEEP_TIME
}

if [ ! -d results ]; then
    mkdir results
else
    rm -fr results/*
fi

rm -f *.log

echo "BENCHMARK FOR LOOPBACK"

python -m $MODULE_NAME -r input -m output -t loopback -l ERROR -sub -re2 > loopback.log 2>&1 &

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

kill_process $MODULE_NAME

for rule in $(ls -1 ./benchmark-rules); do

    for guard_size in 2 4 8 16 32 64 128 256; do

        echo "BENCHMARK FOR $MODULE_NAME $rule $guard_size"

        python -m $MODULE_NAME -r input -m output -t $MODULE_NAME -s benchmark-rules/$rule -l ERROR -sub -re2 -g $guard_size &

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

        kill_process $MODULE_NAME
    done
done
