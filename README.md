# Sage Spotted Lanternfly Detector Example

This repo shows a minimal example of combining YOLO and BioCLIP to attempt to detect spotted lanternflies.

The main content of the example is in the [detect](./detect) script and a similar but not quite identical Python version is in [detect.py](./detect.py).

## Setup

You'll need to setup a virtual environment and install the dependencies one time before running the app.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Now, you simply need to activate the virtual environment before running the app.

```sh
source .venv/bin/activate
```

_I'm also using [duckdb](https://duckdb.org) to show the CSV results. That is currently installed on the Sage nodes out of the box but you may need to install it for local testing._

## Running

You can test the app as follows:

First, put a set of test .jpg files in the `inputs/` directory.

Now, run the app using:

```sh
./detect
```

This will create a `runs/timestamp/` directory with the processed images and results CSV in it.

_Note that during the first run, the required models will be fetched so it may take a bit longer than subsequent runs._

## Results

Each run will produce a `runs/timestamp/` directory with the following artifacts:

* `yolo/*.jpg`: Each input image annotated with YOLO detection bounding boxes and scores.
* `yolo/crops/*/*.jpg`: The crops produced from the YOLO detections.
* `bioclip-results.csv`: A CSV containing the top BioCLIP predictions for each of the crops.
