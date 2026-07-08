# Detecting and Highlighting Terminals on Digital Templates Using AI

Welcome to the project wiki. This is a hybrid **computer-vision + AI** system that automatically detects **missing terminals (clamps)** on digital control-cabinet templates and highlights them for rework operators — turning a slow, error-prone manual inspection into a sub-one-minute automated check.

The system accompanies a Master's thesis in **Software Engineering for Industrial Applications**. It implements a **Detection & Highlighting (D&H)** pipeline that inspects the digital template (blueprint) of a manufacturing order, works out which terminals are missing, and draws red boxes around them so an operator can fix the order quickly.

![Missing terminals highlighted with red boxes](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/missing_terminals_highlighted.jpg)

---

## What you'll find in this wiki

| Page | What it covers |
|------|----------------|
| **[Background & Problem](Background-and-Problem)** | Why manual terminal inspection is a bottleneck and what this system replaces |
| **[How It Works](How-It-Works)** | The end-to-end pipeline: detection → slicing → OCR → matching → annotation |
| **[Architecture](Architecture)** | The three loosely-coupled components and how C# talks to Python |
| **[Tech Stack](Tech-Stack)** | Every library and tool used, and why |
| **[Results](Results)** | Model metrics, OCR accuracy, and end-to-end timing |
| **[Installation](Installation)** | Prerequisites and setup for the Python AI module |
| **[Usage](Usage)** | Running detection/highlighting and retraining the detector |
| **[Project Structure](Project-Structure)** | What lives where in the repository |
| **[Limitations & Future Work](Limitations-and-Future-Work)** | Known gaps and where the project can go next |
| **[FAQ](FAQ)** | Quick answers to common questions |

---

## At a glance

- **Goal:** detect missing terminals on a digital template and highlight them for a rework operator.
- **Approach:** a hybrid pipeline — YOLOv5 finds *where* the position numbers are, Tesseract OCR reads *what* they are, and the two signals are fused.
- **Speed:** the full detect-and-highlight cycle for one order completes in **under a minute** (~44 s in a representative run).
- **Accuracy:** YOLOv5 mAP@0.5 ≈ **0.993**, OCR read accuracy **> 95%**, overall system accuracy **> 90%**.
- **Integration:** runs in-process inside a C# / .NET (Blazor) host via a Python.NET bridge — no network round-trip.

> **New here?** Start with **[Background & Problem](Background-and-Problem)**, then read **[How It Works](How-It-Works)**.
