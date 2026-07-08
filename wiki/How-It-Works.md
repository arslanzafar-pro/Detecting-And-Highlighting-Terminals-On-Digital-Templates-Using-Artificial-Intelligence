# How It Works

The system is a **hybrid pipeline**. An object-detection model finds *where* the terminal-position numbers live on the template, and an OCR model reads *what those numbers are*. The two signals are fused to locate and mark the missing terminals.

> **Input note:** the order template arrives as a **PDF**. The first thing the pipeline does (`pdf_to_images()`) is convert it to images with `pdf2image` + **Poppler**, letterboxing each page to the `640×640` format YOLOv5 expects. Everything below then runs on that image.

## The pipeline, step by step

### 1. Object detection (YOLOv5)
`initial_yolo_detection()` runs a YOLOv5 model — trained from scratch on annotated templates — to locate the strip of the template that contains the terminal **position numbers** (the single class `OneClassNumbers`). It calls `yolov5.detect.run(..., save_crop=True)`, and the detected region is cropped out of the full template. Keeping only high-confidence detections suppresses noise.

### 2. Slicing
`cut_image_into_sub_parts(..., num_parts=7)` splits the cropped strip into **seven vertical segments**. The full number strip is long and dense, which hurts OCR accuracy, so each smaller segment is cleaner and more readable. The horizontal offset of each slice (`max_x`) is tracked so coordinates can later be mapped back onto the full strip.

### 3. OCR (Tesseract)
`ocr_recognize_and_highlight()` pre-processes each segment and reads it with Tesseract:

- convert to **grayscale**
- apply a **sharpening kernel**
- apply **Otsu thresholding** (`THRESH_BINARY + THRESH_OTSU`)
- run Tesseract with `--oem 3 --psm 6`, returning each token's text plus its `left/top/width/height`

Each detected number's X is corrected by its slice offset (`adjusted_x = x + max_x_dict[idx]`) so the coordinates map back onto the *original* template.

### 4. Matching
The OCR tokens are filtered to those that are digits **and** exactly match one of the **missing** terminal numbers from the metadata (an `^{num}$` regex per missing number). Only exact matches are carried forward for annotation.

### 5. Annotation (OpenCV)
OpenCV's `cv2.rectangle(...)` draws **red boxes** (`(0, 0, 254)`) at the matched coordinates on the original image, producing an annotated template that clearly shows which terminals still need to be placed. The result is written to `wwwroot/images/highlighted_image_from_AI/missing_number_image.jpg`.

### 6. Return
The function returns the annotated image's filename, which the host application displays to the operator alongside the list of missing positions.

---

## Pipeline in pictures

**1. Input — a digital order template**

The system starts from a static template (delivered as a PDF) describing where every terminal should sit on the DIN rail.

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
