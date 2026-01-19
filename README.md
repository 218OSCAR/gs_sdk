# GelSight SDK
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) &nbsp;[<img src="assets/rpl.png" height=20px>](https://rpl.ri.cmu.edu/)

This repository is a modified version of the [the official gsrobotics implementation](https://github.com/gelsightinc/gsrobotics), offering improvements in usability and sensor compatibility.

## Key Features

- **Sensor Calibration**: Added functionality for users to calibrate their own GelSight sensors.

- **Expanded Sensor Compatibility**: Compatible with other GelSight sensors, including Digit and lab-made sensors.

- **Low-Latency Sensor Reading**: Including an enhanced image streaming pipeline for reduced latency and frame drop, especially for GelSight Mini.

    ⚠️ The original streaming implementation uses OpenCV and may drop to ~10 Hz. The low-latency version uses FFmpeg to maintain 25 Hz, **but on some systems it can introduce severe frame delay and duplication**. Contributions to improve this are welcome via Pull Request.


Authors:
* [Hung-Jui Huang](https://joehjhuang.github.io/) (hungjuih@andrew.cmu.edu)
* Ruihan Gao (ruihang@andrew.cmu.edu)

## Support System
* Tested on Ubuntu 22.04
* Tested on GelSight Mini and Digit
* Python >= 3.9

## Installation
Clone and install gs_sdk from source:
```bash
git clone git@github.com:joehjhuang/gs_sdk.git
cd gs_sdk
pip install -e .
```

## Coordinate Conventions
The coordinate system convention in this SDK is shown below, using the GelSight Mini sensor for illustration:

| 2D (sensor image)                           | 3D                         |
| --------------------------------- | --------------------------------- |
| <img src="assets/gsmini_frame_2D.png" width="200"/>  | <img src="assets/gsmini_frame_3D.png" width="200"/>    |

## Sensor Calibration
For more details on sensor calibration, see the [Calibration README](calibration/README.md).

## Examples
These examples show basic usage of this GelSight SDK.
### Sensor Streaming
Stream images from a connected GelSight Mini:
```python
python examples/stream_device.py
```

### Low Latency Sensor Streaming
Stream images with low latency and without frame dropping from a connected GelSight Mini:
```python
python examples/fast_stream_device.py
```

### Reconstruct Touched Surface
Reconstruct a touched surface using the calibration model. Calibration steps are detailed in the [Calibration README](calibration/README.md).
```python
python examples/reconstruct.py
```
The reconstructed surface will be displayed and saved in `examples/data`.

## Extensions in This Fork: Multi-GelSight Support

This fork extends the original **gs_sdk** with **robust support for multiple GelSight sensors on a single machine** (e.g., left/right fingers).

The main challenge is that a single GelSight device exposes **multiple `/dev/video*` nodes**, and multiple sensors of the same model cannot be reliably distinguished by index alone.  
This fork introduces **deterministic device resolution** based on **hardware-bound device names and stream capability detection**.

---

### What’s New

- **Deterministic device selection**  
  Each physical GelSight sensor is identified by its V4L2 device name (e.g. `GelSight Mini R0B 2DE9-0HLG: Ge`).

- **Automatic stream resolution**  
  Among multiple `/dev/video*` nodes, the SDK automatically selects the true image stream based on supported resolution (e.g. `3280×2464`).

- **YAML-based per-device configuration**  
  Each physical sensor is configured via its own YAML file, making multi-sensor setups clean and scalable.

---

### YAML Configuration (Recommended)

Each physical GelSight sensor should have **one YAML file**.

#### Example: `gsmini_left.yaml`

```yaml
device_name: "GelSight Mini R0B 2DDZ-43PB: Ge"

ppmm: 0.0634

imgh: 240
imgw: 320

raw_imgh: 2464
raw_imgw: 3280
framerate: 25
