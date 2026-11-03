# Sage Spotted Lanternfly Detector Example

This repo shows a minimal example of combining YOLO and Bioclip to attempt to detect spotted laternflies.

## Setup

You'll need to setup a virtual environment and installed the dependencies one time before running the app.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Now, you simply need to activate the virtual environment before running the app.

```sh
source .venv/bin/activate
```

## Running

You can test the app as follows:

First, put a set of test .jpg files in the `inputs/` directory.

Now, run the app using:

```sh
./detect
```

This will create a `runs/epochtime` directory with the processed images and results CSV in it. Note that during the first run, the required models will be fetched so it may take a bit longer than subsequent runs.
