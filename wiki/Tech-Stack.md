# Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Object detection** | YOLOv5 (Ultralytics, PyTorch) | Locates the terminal position-number region (`OneClassNumbers`) on the template |
| **Text recognition** | Tesseract OCR (via `pytesseract`) | Reads the position numbers and returns their X, Y coordinates |
| **PDF → image** | `pdf2image` + Poppler | Converts the order PDF into images the pipeline can process |
| **Image processing** | OpenCV, NumPy, Pillow | Letterboxing, slicing, coordinate mapping, and drawing the red boxes |
| **C# ↔ Python bridge** | Python.NET (`pythonnet`) | Runs the Python models in-process from the C# host |
| **Host application** | C# / .NET, Blazor | Rework UI, order metadata, and rendering the annotated result |
| **Annotation tooling** | LabelImg | Used to build the annotated YOLOv5 training set |

## Notes on key choices

- **YOLOv5** was chosen for its **stability** and mature tooling rather than being the newest model available — a deliberate trade-off for a system intended to move toward production. See [Limitations & Future Work](Limitations-and-Future-Work) for the upgrade path.
- **Tesseract** is a system binary; the `pytesseract` package is only a thin Python wrapper around it, so Tesseract must be installed separately (see [Installation](Installation)).
- **Poppler** is likewise an external binary that `pdf2image` shells out to; its path is set via `POPPLER_PATH` in the script.
- **Python.NET** keeps the AI models running **in the same process** as the C# host, avoiding a network hop between the application and the inference code.
- **LabelImg** was used during dataset preparation to draw the bounding-box annotations that YOLOv5 trained on.

> **On `requirements.txt`:** the file shipped in the repo is the standard **YOLOv5** requirements set (torch, torchvision, opencv-python, numpy, pillow, ultralytics, …). The extra runtime packages the pipeline imports — `pytesseract`, `pdf2image`, and `pythonnet` — are **not** listed there and must be installed separately (see [Installation](Installation)).

---

**Next:** [Results →](Results)
