# Background & Problem

## The manufacturing context

In the manufacturing of **electrical control cabinets**, robotic arms place **terminals** (also called *clamps*) onto a **DIN rail** according to a pre-generated **digital template**. The template is the blueprint that says exactly which terminal should sit at which position on the rail.

After the robotic placement step, a **human operator** has to verify that every terminal was placed correctly. They do this by comparing the static template against the order's metadata, position by position. This manual check is:

- **Slow** — it is repetitive and has to be done for every order.
- **Hard to scale** — throughput is bounded by operator attention, not machine speed.
- **Error-prone** — small mismatches are easy to miss when scanning dense number strips by eye.

## Why a normal camera-vision system doesn't fit

A classic camera-based inspection system watches a physical scene through a live feed. That approach **cannot be applied directly here**, because the process works from **already-generated digital templates**, not a camera view of the physical cabinet.

This project turns that constraint into an advantage. Instead of adding cameras and lighting rigs, it runs **entirely on the existing template images plus the order metadata**. That makes inspection:

- **Faster** — no capture step, it operates on data that already exists.
- **Cheaper** — no additional hardware on the line.
- **More reliable** — the input is a clean digital image, not a noisy physical scene.

## What the system delivers

The **Detection & Highlighting (D&H)** system was built to:

- **Detect** missing terminals on a digital template by cross-checking it against the order's metadata.
- **Highlight** the missing terminals with red bounding boxes so they are obvious at a glance.
- **Integrate** into the existing rework workflow, triggering automatically when an operator opens an order's rework page.
- **Return results fast** — the full detect-and-highlight cycle for one order completes in **under a minute**.

The net effect: an inspection that used to depend on careful manual comparison becomes an automated check that finishes in seconds and points the operator straight at what needs fixing.

---

**Next:** [How It Works →](How-It-Works)
