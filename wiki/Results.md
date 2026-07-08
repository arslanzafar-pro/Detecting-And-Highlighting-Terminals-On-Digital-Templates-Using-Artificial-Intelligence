# Results

The models and the end-to-end pipeline were evaluated on **real order templates**.

## YOLOv5 — position-number detection

| Metric | Value |
|--------|-------|
| Precision | ~0.995 |
| Recall | ~0.996 |
| mAP@0.5 | 0.993 |
| Training set | 231 annotated templates (70% train / 20% val / 10% test) |

The precision, recall, and F1 curves all sit very close to **1.0** at low-to-mid confidence thresholds, with **no significant gap** between training and validation loss — i.e. **no overfitting** was observed.

## OCR & end-to-end

| Metric | Value |
|--------|-------|
| OCR position-read accuracy | > 95% |
| End-to-end detect + highlight time | < 1 minute (44 s in a representative run) |
| Overall system accuracy (across test cases) | > 90% |

## How to read these numbers

- **High precision + high recall** on the detector means the position-number region is found almost every time, with very few false positives — which matters because everything downstream depends on that crop being correct.
- **Slicing before OCR** is a big contributor to the **> 95%** read accuracy: reading seven small, clean segments beats reading one long, dense strip.
- The **< 1 minute** end-to-end figure is the whole point of the system — it replaces a slow manual comparison with a check that finishes while the operator is still looking at the screen.

---

**Next:** [Installation →](Installation)
