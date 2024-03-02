#!/usr/bin/bash

source sd-scripts/venv/bin/activate

function usage {
    echo "$0 starts kohya trainer and tensorboard."
    echo "usage: $0 [config folder] <additional kohya options>"
}

CONFIG=$1
LOGDIR=$CONFIG/logs

mkdir $LOGDIR

shift

(
    trap 'kill 0' SIGINT;
    accelerate launch --num_cpu_threads_per_process 8 sd-scripts/sdxl_train_network.py \
    --config_file="$CONFIG/config.toml" \
    --dataset_config="$CONFIG/dataset.toml" \
    --log_with tensorboard --logging_dir="$LOGDIR" $@ \
    & tensorboard --logdir="$LOGDIR" --host 192.168.0.2 & wait
)
