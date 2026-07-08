# Installation

> The core inspection pipeline is the **Python AI module**. The C# host application integrates it via Python.NET. The steps below set up the Python side, which you can run and test on its own.

## Prerequisites

- **Python 3.13**
- **Git** and **[Git LFS](https://git-lfs.com/)** — the trained weights and sample templates are large binary files, so clone with LFS enabled.
- **Tesseract OCR** installed as a system binary (the `pytesseract` package is only a wrapper around it):
  - **Windows:** download the installer from the [Tesseract at UB Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS:** `brew install tesseract`
  - **Linux:** `sudo apt install tesseract-ocr`
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

# 3. Install Python dependencies
pip install -r requirements.txt
```

If a `requirements.txt` isn't present, install the core packages directly:

```bash
pip install torch torchvision opencv-python numpy pytesseract pythonnet ultralytics
```

## Tesseract path note

If Python can't find the Tesseract binary, point to it explicitly in your script:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

> **Why Git LFS matters:** without it, cloning pulls down small text *pointer* files instead of the actual model weights and sample templates, and inference will fail. Run `git lfs install` **before** cloning.

---

**Next:** [Usage →](Usage)
