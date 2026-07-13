# Software Directory

This directory contains software for OpenEUV system control, simulation, and metrology.

## Directory Structure

```
software/
├── control/             # Real-time control and simulation
│   └── stage_servo_sim.py       # Stage servo loop simulation
├── simulation/          # Optical and system simulation
│   ├── requirements.txt         # Python dependencies
│   └── euv_source_model.py      # (placeholder) LPP source spectral model
└── metrology/           # Metrology data processing
    └── wavefront.py             # (placeholder) Wavefront analysis
```

## Getting Started

### Install Dependencies

```bash
pip install -r software/simulation/requirements.txt
```

### Run Simulations

```bash
# Collector mirror efficiency calculation
python simulations/optical/collector_efficiency.py

# Projection optics PSF and MTF
python simulations/optical/projection_psf.py

# Stage servo simulation
python software/control/stage_servo_sim.py
```

## Simulation Modules

| Module | Location | Description |
|---|---|---|
| `collector_efficiency.py` | `simulations/optical/` | EUV power budget from source to IF |
| `projection_psf.py` | `simulations/optical/` | PSF, MTF, Strehl, resolution |
| `stage_servo_sim.py` | `software/control/` | Stage servo, sync error simulation |

## Software Architecture

See [`docs/design/09_control_system.md`](../docs/design/09_control_system.md) for the full control system design.

| Layer | Technology | Location |
|---|---|---|
| FPGA servo | VHDL/Verilog | `hardware/control/fpga_boards/` |
| Real-time sequencer | C++ (RTOS) | (future: `software/control/`) |
| Supervisory | Python 3.10+ | (future: `software/supervisory/`) |
| HMI | PyQt or web | (future: `software/hmi/`) |
| Simulation | Python 3.10+ | `software/simulation/`, `simulations/` |
