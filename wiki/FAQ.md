# FAQ

**What exactly is a "terminal"?**
A terminal (also called a *clamp*) is a component that a robotic arm places onto a DIN rail when building an electrical control cabinet. The system checks that all required terminals are present on the order.

**Why not just use a camera to inspect the physical cabinet?**
Because the process works from **already-generated digital templates**, not a live physical scene. A camera-based system doesn't fit; running on the existing template images is faster, cheaper, and more reliable. See [Background & Problem](Background-and-Problem).

**What's the input — an image or a PDF?**
A **PDF**. The pipeline's first step converts it to images with `pdf2image` + Poppler, then runs detection on those images. See [How It Works](How-It-Works).

**Why combine YOLOv5 *and* Tesseract instead of one model?**
They do different jobs. YOLOv5 finds *where* the position-number region is; Tesseract reads *what* the numbers are. Fusing "location" and "value" is what lets the system map a missing position back to exact coordinates. See [How It Works](How-It-Works).

**Why slice the strip into seven pieces before OCR?**
The full number strip is long and dense, which hurts OCR accuracy. Reading seven small, clean segments and then stitching the coordinates back together gives far better results (> 95% read accuracy). See [How It Works](How-It-Works).

**How does it decide what to highlight?**
It only draws a box where an OCR-read token is a digit **and** exactly matches one of the missing numbers passed in from the order metadata. See [How It Works](How-It-Works).

**How fast is it?**
The full detect-and-highlight cycle for one order runs in **under a minute** — 44 seconds in a representative run. See [Results](Results).

**How accurate is it?**
YOLOv5 mAP@0.5 ≈ 0.993, OCR read accuracy > 95%, and overall system accuracy > 90% across test cases. See [Results](Results).

**Do I need a GPU?**
No — inference runs on CPU. A GPU with CUDA is only recommended if you want to retrain the detector. See [Installation](Installation).

**Why do I need Git LFS to clone it?**
The trained weights and sample templates are large binary files tracked via Git LFS. Without `git lfs install` before cloning, you get pointer files instead of the real assets and inference fails. See [Installation](Installation).

**How does the Python code run inside a C# app?**
Through a **Python.NET** bridge that runs the models in-process — no network round-trip between the host and the inference code. See [Architecture](Architecture).

**It won't run on my machine — why?**
Most likely the hard-coded paths in `myPythonScript.py` (Poppler, YOLOv5 weights, `temp_images`) still point at the original dev machine. Update them for your environment. See [Installation](Installation) and [Limitations & Future Work](Limitations-and-Future-Work).

**What license is this under?**
The project builds on **Ultralytics YOLOv5**, which is distributed under **AGPL-3.0**. If you redistribute a derivative that includes YOLOv5, your combined work may need to comply with AGPL-3.0. Review [Ultralytics' licensing](https://docs.ultralytics.com/models) before publishing under a different license.

**Who built this?**
[Arslan Zafar](https://www.linkedin.com/in/arslanzafar-pro/), as part of a Master's thesis in Software Engineering for Industrial Applications.
