# How It Works

The system is a **hybrid pipeline**. An object-detection model finds *where* the terminal-position numbers live on the template, and an OCR model reads *what those numbers are*. The two signals are fused to locate and mark the missing terminals.

## The pipeline, step by step

### 1. Object detection (YOLOv5)
A YOLOv5 model — trained from scratch on annotated templates — locates the strip of the template that contains the terminal **position numbers**. Only detections above a **confidence threshold of `0.80`** are kept, which suppresses noise. The detected region is then cropped out of the full template.

### 2. Slicing
The full number strip is long and dense, which hurts OCR accuracy. The cropped strip is therefore sliced programmatically into **seven vertical segments** so each piece is clean and readable.

### 3. OCR (Tesseract)
Each segment is pre-processed (**grayscale + adaptive thresholding**) and passed to Tesseract OCR, which returns each **position number together with its X, Y coordinates**. The seven slices are then stitched back together in code so the coordinates map back onto the *original* template.

### 4. Matching
The list of numbers the OCR extracted is compared against the metadata list of **missing** terminal positions. Where a missing position matches an OCR-read number, its coordinates are handed off for annotation.

### 5. Annotation (OpenCV)
OpenCV draws **red bounding boxes** at the matched coordinates on the original template, producing an annotated image that clearly shows the operator which terminals still need to be placed.

### 6. Return
The annotated template is passed back to the host application and displayed to the operator alongside a list of the missing positions.

---

## Pipeline in pictures

**1. Input — a digital order template**

The system starts from a static template describing where every terminal should sit on the DIN rail.

![Digital template used as input](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/digital_template_input.jpg)

**2. Cropping — the cropped strip for OCR**

The detected object class is cropped, ready to be sliced and handed to OCR so it can read the numbers and return their X, Y coordinates.

![One cropped image for reading through OCR](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/Cropped_Image.jpg)

**3. Slicing — the cropped strip is split into 7 segments**

Each segment is small and clean, which gives Tesseract far better accuracy than reading the whole strip at once.

![Slice 1](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/cropped_Slice_1.jpg)
![Slice 2](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/cropped_Slice_2.jpg)
![Slice 3](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/cropped_Slice_3.jpg)
![Slice 4](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/cropped_Slice_4.jpg)
![Slice 5](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/cropped_Slice_5.jpg)
![Slice 6](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/cropped_Slice_6.jpg)
![Slice 7](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/cropped_Slice_7.jpg)

**4. Detection — YOLOv5 locates the position-number region**

The trained model detects the region containing the terminal position numbers (shown highlighted) and crops it for further processing.

![YOLOv5 detecting the position-number region](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/terminal_detection.jpg)

**5. Output — missing terminals highlighted**

After matching OCR results against the metadata, the missing terminals are marked with red boxes on the original template.

![Missing terminals highlighted with red boxes](https://raw.githubusercontent.com/arslanzafar-pro/Detecting-And-Highlighting-Terminals-On-Digital-Templates-Using-Artificial-Intelligence/main/assets/images/missing_terminals_highlighted.jpg)

---

**Next:** [Architecture →](Architecture)
