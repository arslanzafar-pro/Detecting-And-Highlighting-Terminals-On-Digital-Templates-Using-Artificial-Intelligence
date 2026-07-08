# Project Structure

## Repository layout

```
.
├── assets/
│   └── images/              # README / wiki illustrations
├── input/                   # sample input (image25Original.jpg)
├── yolov5/                  # YOLOv5 training / inference setup (train.py, detect.py, models, weights)
├── poppler-24.07.0/         # bundled Poppler binaries (PDF → image support)
├── Lib/                     # committed virtual-environment library files
├── Scripts/                 # committed virtual-environment scripts
├── share/                   # supporting resources
├── __pycache__/             # Python bytecode cache
├── convert.ipynb            # notebook (template/format conversion & experiments)
├── myPythonScript.py        # main pipeline: PDF → detect → slice → OCR → highlight
├── requirements.txt         # YOLOv5 Python dependencies
├── pyvenv.cfg               # virtual-environment config
└── README.md
```

## Where the important pieces live

| Path | What it holds |
|------|---------------|
| `myPythonScript.py` | The main script that drives the whole pipeline. Key functions: `pdf_to_images`, `letterbox`, `initial_yolo_detection`, `cut_image_into_sub_parts`, `ocr_recognize_and_highlight`, and `main`. |
| `yolov5/` | The YOLOv5 setup used for training the detector and running inference (`detect.py` is imported as `from yolov5.detect import run`). |
| `input/` | Sample order template(s) — e.g. `image25Original.jpg`. |
| `assets/images/` | The illustration images used in the README and this wiki. |
| `poppler-24.07.0/` | Bundled Poppler, used by `pdf2image` to convert PDF templates into images. |
| `convert.ipynb` | A notebook for conversion / experimentation. |
| `requirements.txt` | The YOLOv5 package list (see note below). |

## Runtime paths the script touches

- **Reads:** the input PDF; the YOLOv5 `best.pt` weights; a `temp_images/` folder where converted PDF pages are written and read back.
- **Writes:** `wwwroot/images/highlighted_image_from_AI/missing_number_image.jpg` — the final annotated image, placed in the Blazor host's static-files directory for display.

> **Note on the committed venv:** `Lib/`, `Scripts/`, `__pycache__/`, `share/`, and `pyvenv.cfg` are part of a committed Python virtual environment. If you set up your own `.venv` (see [Installation](Installation)), you can ignore these — and they'd normally be `.gitignore`d in a fresh clone.

> **Note on `requirements.txt`:** it's the standard YOLOv5 requirements set. The extra packages the pipeline imports — `pytesseract`, `pdf2image`, `pythonnet` — are not listed there; install them separately.

---

**Next:** [Limitations & Future Work →](Limitations-and-Future-Work)
