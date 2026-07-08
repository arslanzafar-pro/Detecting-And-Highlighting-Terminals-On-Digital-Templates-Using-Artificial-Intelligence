# Installation

> The core inspection pipeline is the **Python AI module** (`myPythonScript.py`). The C# host application integrates it via Python.NET. The steps below set up the Python side, which you can run and test on its own.

## Prerequisites

- **Python 3.13**
- **Git** and **[Git LFS](https://git-lfs.com/)** — the trained weights and sample templates are large binary files, so clone with LFS enabled.
- **Tesseract OCR** installed as a system binary (the `pytesseract` package is only a wrapper around it):
  - **Windows:** download the installer from the [Tesseract at UB Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS:** `brew install tesseract`
  - **Linux:** `sudo apt install tesseract-ocr`
- **Poppler** — required by `pdf2image` to convert the order PDF to images:
  - **Windows:** download a Poppler build and note its `Library\bin` path (a copy ships in the repo under `poppler-24.07.0/`)
  - **macOS:** `brew install poppler`
  - **Linux:** `sudo apt install poppler-utils`
- *(Optional, for retraining)* an **NVIDIA GPU with CUDA** — inference also runs on CPU.

## Steps

```bash
# 1. Clone (with Git LFS so the weights come down, not just pointers)
git lfs install
git clone https://github.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence.git
cd Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence

# 2. Create and activate a virtual environment
python -m venv .venv

#    Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    macOS / Linux:
source .venv/bin/activate

# 3. Install the YOLOv5 dependencies
pip install -r requirements.txt

# 4. Install the extra runtime packages the pipeline imports
#    (these are NOT in requirements.txt)
pip install pytesseract pdf2image pythonnet
```

## Configure the local paths

`myPythonScript.py` contains **absolute paths from the original development machine**. Update them before running:

| Location | What to set |
|----------|-------------|
| `POPPLER_PATH` (in `pdf_to_images()` and `main()`) | Your Poppler `Library\bin` directory |
| `weights=...best.pt` (in `initial_yolo_detection()`) | Path to your trained YOLOv5 weights |
| `directory` (in `ocr_recognize_and_highlight()`) | The `temp_images` folder the converted page is read back from |

## Tesseract path note

If Python can't find the Tesseract binary, point to it explicitly in your script:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

> **Why Git LFS matters:** without it, cloning pulls down small text *pointer* files instead of the actual model weights and sample templates, and inference will fail. Run `git lfs install` **before** cloning.

---

**Next:** [Usage →](Usage)
