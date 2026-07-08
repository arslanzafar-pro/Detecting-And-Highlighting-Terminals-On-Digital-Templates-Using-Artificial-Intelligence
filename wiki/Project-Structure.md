# Project Structure

## Repository layout

```
.
├── assets/
│   └── images/              # README / wiki illustrations
├── Lib/                     # virtual-environment library files
├── Scripts/                 # virtual-environment scripts
├── share/                   # supporting resources
├── input/                   # sample input templates
├── poppler-24.07.0/         # Poppler binaries (PDF → image support)
├── yolov5/                  # YOLOv5 training / inference setup
├── convert.ipynb            # notebook (e.g. template/format conversion)
├── myPythonScript.py        # main Python entry point / pipeline logic
├── requirements.txt         # Python dependencies
├── pyvenv.cfg               # virtual-environment config
└── README.md
```

## Where the important pieces live

| Path | What it holds |
|------|---------------|
| `myPythonScript.py` | The main Python script that drives the detect → slice → OCR → match → annotate pipeline. |
| `yolov5/` | The YOLOv5 setup used for training the detector and running inference (includes `train.py`, model configs, and weights). |
| `input/` | Sample order templates to run the pipeline against. |
| `assets/images/` | The illustration images used in the README and this wiki. |
| `poppler-24.07.0/` | Poppler, used for converting PDF templates into images the pipeline can process. |
| `convert.ipynb` | A notebook for conversion / experimentation. |
| `requirements.txt` | The Python package list for setting up the environment. |

> **Note:** `Lib/`, `Scripts/`, and `pyvenv.cfg` are part of a committed Python virtual environment. If you clone and set up your own `.venv` (see [Installation](Installation)), you can ignore these.

## Conceptual structure (from the README)

The logical layout of the codebase is:

```
.
├── assets/images/           # illustrations
├── weights/                 # trained YOLOv5 weights (best.pt) — via Git LFS
├── <python-ai-module>/      # detection, slicing, OCR, annotation logic
├── <yolov5>/                # YOLOv5 training/inference setup
├── requirements.txt
└── README.md
```

---

**Next:** [Limitations & Future Work →](Limitations-and-Future-Work)
