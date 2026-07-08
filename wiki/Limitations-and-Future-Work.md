# Limitations & Future Work

## Known limitations

- **Blurring of irrelevant data is not yet fully working.** It was specified as a feature, but the annotated output currently keeps the surrounding template visible rather than blurring everything except the missing terminals.
- **OCR is tuned for clean, structured templates.** It reads numeric positions well when the template is clear and well-structured, but is not yet robust to alphabetic text, lower-contrast layouts, or unfamiliar formats.

## Future work

- **Newer detector.** YOLOv5 was chosen for stability; the pipeline can be retrained on a newer YOLO release for better speed/accuracy once one is stable for production.
- **Adaptive OCR.** Extend OCR to handle alphabetic text, lower-contrast layouts, and new template formats — potentially assisted by an LLM.
- **Continuous learning.** Feed error logs back into the models so they adapt to new template types over time.
- **Hardware & scaling.** A stronger GPU plus a load balancer would let the system handle many concurrent inspection requests.
- **Finish the blurring feature.** Complete the "blur everything except the missing terminals" behavior so the operator's attention is drawn only to what needs rework.

---

**Next:** [FAQ →](FAQ)
