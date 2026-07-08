# Usage

The Python AI module has **no CLI/argparse**. The entry point is the `main()` function in `myPythonScript.py`, which the C# host calls through the Python.NET bridge. It takes an **order PDF** and the **list of missing terminal numbers**, and returns the path to the highlighted output image.

## Entry point

```python
# myPythonScript.py
def main(_input_pdf, missing_numbers):
    ...
    return path   # -> "missing_number_image.jpg"
```

| Argument | Meaning |
|----------|---------|
| `_input_pdf` | Path to the order template **PDF** |
| `missing_numbers` | List of terminal position numbers that are missing (from the order metadata) |

The function returns the filename of the annotated image, which is written to
`wwwroot/images/highlighted_image_from_AI/missing_number_image.jpg` (the Blazor host's static-files folder).

## What `main()` does

1. **`pdf_to_images(pdf_file)`** — converts the PDF to images using `pdf2image` + **Poppler**, letterboxing each page to the `640×640` format YOLOv5 expects.
2. **`initial_yolo_detection(images)`** — runs `yolov5.detect.run(...)` with `save_crop=True` to detect the `OneClassNumbers` region and crop it out.
3. **`cut_image_into_sub_parts(detect_Images, num_parts=7)`** — slices the cropped strip into 7 vertical parts.
4. **`ocr_recognize_and_highlight(cropped_parts, original_image, missing_numbers)`** — OCRs each slice, matches numbers against `missing_numbers`, and draws red boxes on the original image.

## Running it standalone

To test outside the C# host, call `main()` directly (see the commented `__main__` block at the bottom of `myPythonScript.py`):

```python
from myPythonScript import main

pdf_file = r"path/to/order_template.pdf"
missing_numbers = [12, 34, 56]          # positions reported missing by the metadata
output = main(pdf_file, missing_numbers)
print(output)                            # missing_number_image.jpg
```

> **Update the hard-coded paths first** — see [Installation → Configure the local paths](Installation). The Poppler path, the YOLOv5 weights path, and the `temp_images` directory are all absolute paths from the original dev machine.

## OCR settings used

Each slice is pre-processed and read with Tesseract:

```python
# grayscale -> sharpening kernel -> Otsu threshold
custom_config = r'--oem 3 --psm 6'
ocr_data = pytesseract.image_to_data(thresholded_image, config=custom_config, output_type=Output.DICT)
```

Only OCR tokens that are digits **and** exactly match a missing number (`^{num}$` regex) are highlighted.

## Retrain the YOLOv5 detector

From the `yolov5/` directory, with your dataset configured in the `.yaml`:

```bash
python train.py --img 640 --epochs 500 --data coco128.yaml --weights yolov5s.pt
```

| Setting | Value |
|---------|-------|
| Classes | **1** (`OneClassNumbers` — the terminal-position region) |
| Input size | `640 × 640` |
| Starting weights | `yolov5s.pt` |
| Best checkpoint | `best.pt` (used for inference) |

---

**Next:** [Project Structure →](Project-Structure)
