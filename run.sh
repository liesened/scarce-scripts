#!/usr/bin/bash

source sd-scripts/venv/bin/activate

function usage {
    echo "$0 starts kohya trainer and tensorboard."
    echo "usage: $0 [config folder] <additional kohya options>"
    exit
}

CONFIGDIR=$1
LOGDIR=$CONFIGDIR/logs

mkdir $LOGDIR

shift

function run_train {
    for CONFIG in "$CONFIGDIR"/config*.toml; do
        echo "Loading $CONFIG"
        accelerate launch --num_cpu_threads_per_process 2 sd-scripts/sdxl_train_network.py \
        --config_file="$CONFIG" \
        --dataset_config="$CONFIGDIR/dataset.toml" \
        --log_with tensorboard --logging_dir="$LOGDIR" $@
    done
}



(
    trap 'kill 0' SIGINT;
    run_train & tensorboard --logdir="$LOGDIR" --host 0.0.0.0 & wait
)

