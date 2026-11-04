#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
from shutil import copyfile
import torch


# autodetect which device to use (CUDA, MPS, or CPU)
device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")


def create_crops(crops_dir: Path):
    from ultralytics import YOLOE
    from ultralytics.utils.plotting import save_one_box

    model = YOLOE("yoloe-26x-seg.pt")
    model.set_classes([
        "insect",
        "bug",
        "black insect with white spots",
        "red and black insect",
        "spotted lanternfly",
    ])

    for r in model.predict("inputs/", conf=0.05, imgsz=1280, agnostic_nms=True, iou=0.5, stream=True, device=device):
        stem = Path(r.path).stem
        for i, box in enumerate(r.boxes):
            save_one_box(
                box.xyxy,                       # box in original-image pixels
                r.orig_img,                     # original image (BGR numpy array)
                file=crops_dir / f"{stem}_{i:03d}.jpg",
                gain=1.5,                       # grow the box 1.5x (~25% each side)
                pad=0,                          # extra fixed pixels on top of gain
                BGR=True,                       # orig_img is BGR, as Ultralytics uses it internally
            )


def classify_crops(crops_dir: Path, classify_dir: Path):
    from bioclip import Rank
    from bioclip.predict import TreeOfLifeClassifier

    classifier = TreeOfLifeClassifier(device=device)

    crops = sorted(crops_dir.glob("*.jpg"))
    predictions = classifier.predict(crops, Rank.SPECIES, k=1)
    for prediction in predictions:
        print(prediction)

        # Skip predictions with low confidence scores.
        accept_prediction = "yes" if prediction["score"] >= 0.8 else "no"

        # Link an entry in the species directory to the cropped image.
        link_path = Path(classify_dir, accept_prediction, prediction["species"], prediction["file_name"].name)
        link_path.parent.mkdir(parents=True, exist_ok=True)
        link_path.hardlink_to(prediction["file_name"])


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    run_dir = Path("runs", now.isoformat())
    crops_dir = Path(run_dir, "crops")
    classify_dir = Path(run_dir, "classify")

    # Run detection pipeline.
    create_crops(crops_dir)
    classify_crops(crops_dir, classify_dir)
