@echo off

call .\sd-scripts\venv\Scripts\activate

set "CONFIG=%1"
set "LOGDIR=%CONFIG%\logs"

mkdir %LOGDIR%

accelerate launch --num_cpu_threads_per_process 2 sd-scripts\sdxl_train_network.py ^
    --config_file="%CONFIG%\config.toml" ^
    --dataset_config="%CONFIG%\dataset.toml" ^
    --log_with tensorboard --logging_dir="%LOGDIR%" %@
