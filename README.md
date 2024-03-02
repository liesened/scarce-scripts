# scarce scripts

These are my personal kohya scripts wrapper for lora training and some other scripts to save myself from kohya and dataset preparation pain, use at your own risk and don't expect >>>Windows<<< support from me.

SD 1.5 is not supported and will never be.

The goal is to focus on encapsulating most of the training stuff inside a single folder for a single bake while relying on sd-scripts functionality. Kind of like [HCP-Diffusion](https://github.com/IrisRainbowNeko/HCP-Diffusion) but in a way more stupid yet broad manner.

Go to [scripts/README.md](scripts/README.md) to see more about the dataset scripts. 

# Installation

To use the training scripts, will you need to install [sd-scripts](https://github.com/kohya-ss/sd-scripts/?tab=readme-ov-file#windows-installation) first. Install them into `sd-scripts` folder.

## sd-scripts

```sh
git clone https://github.com/liesened/scarce-scripts.git
cd scarce-scripts

git clone https://github.com/kohya-ss/sd-scripts.git
cd sd-scripts

python -m venv venv
```

Depending on the platform, activate the venv, install pytorch and bitsandbytes. On Windows, do

```bat
.\venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install --upgrade -r requirements.txt
pip install -U xformers --index-url https://download.pytorch.org/whl/cu121
python -m pip install bitsandbytes==0.41.1 --prefer-binary --extra-index-url=https://jllllll.github.io/bitsandbytes-windows-webui
```

On Linux, do

```sh
. venv/bin/activate
pip install torch torchvision
pip install --upgrade -r requirements.txt
pip install xformers bitsandbytes
```

Run through accelerate config. See [kohya instructions](https://github.com/kohya-ss/sd-scripts/?tab=readme-ov-file#windows-installation) on how to answer this.

```sh
accelerate config
```

## scarce-scripts

After answering the config, while still inside the `sd-scripts` folder and inside the virtual python environment, do this.

```sh
cd ..
pip install --upgrade -r requirements.txt
```

# Basic Usage

Imagine this folder structure:

```
- configs/  -- this is where all the configs are stored
    - sparkle/  -- the root "concept" folder
        - outputs/  -- lora training artifacts, created automatically
        - config.toml  -- the config file, read by kohya scripts directly
        - dataset.toml  -- same as above, but for datasets
        - logs/  -- tensorboard logs, created automatically
```

This allows (re)baking the model simply by modifying the corresponding config files and running

```sh
./run.sh configs/sparkle
```

You can store more loras like this:

```
- configs/
    - sparkle/
        - config.toml
        - dataset.toml
    - hoshino/
        - config.toml
        - dataset.toml
    - ...
```

## Tips

### Multiple configs per lora

```
- configs/
    - sparkle/
        - outputs/
        - lion/
            - config.toml
            - dataset.toml
        - adamw/
            - config.toml
            - dataset.toml
        - logs/
```

Run respective configs like this:

```sh
./run.sh configs/sparkle/lion
./run.sh configs/sparkle/adamw
```

---

### Test loras without copying them

You can make a link that will point to the lora folder of the ui of choice.
Windows, **CMD**:

```bat
mklink /J configs\sparkle\outputs  E:\webui\models\Lora\sparkle
```

Linux: use `ln -s`

If you don't want to use symlinks, you can always add a kohya parameter to `run.sh`:

```sh
./run.sh configs/sparkle/lion --output_dir "/home/whoever/webui/models/Lora/sparkle"
```
