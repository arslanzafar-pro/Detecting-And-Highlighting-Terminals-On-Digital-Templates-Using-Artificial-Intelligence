# Usage

> Replace the script/entry-point names below with the actual filenames in the repo.

## Run detection + highlighting on a single template

```bash
python detect.py --template path/to/order_template.jpg --weights weights/best.pt
```

This runs the full pipeline on one template: detect the position-number region, slice it, OCR the numbers, match against the missing-terminal metadata, and draw the red boxes. See [How It Works](How-It-Works) for what happens at each stage.

## Retrain the YOLOv5 detector

From the YOLOv5 directory, with your dataset configured in the `.yaml`:

```bash
python train.py --img 640 --epochs 500 --data coco128.yaml --weights yolov5s.pt
```

### Training configuration used

| Setting | Value |
|---------|-------|
| Classes | **1** (`OneClassNumbers` — the terminal-position region) |
| Input size | `640 × 640` |
| Starting weights | `yolov5s.pt` |
| Best checkpoint | `best.pt` (used for inference) |

The single-class setup keeps the detector focused on one job: finding the number strip. The `best.pt` checkpoint produced during training is the one loaded at inference time.

## Confidence threshold

At inference, only detections above a **confidence of `0.80`** are kept. This suppresses noisy, low-confidence boxes so that only the true position-number region is cropped and passed downstream.

---

**Next:** [Project Structure →](Project-Structure)
