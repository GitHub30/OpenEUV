# Hardware Directory

This directory contains hardware design files for OpenEUV subsystems.

## Directory Structure

```
hardware/
├── euv_source/          # EUV source mechanical designs
│   ├── source_chamber/  # Chamber CAD drawings (.FCStd, .STEP)
│   ├── droplet_gen/     # Droplet generator design files
│   └── debris_trap/     # Debris mitigation hardware
├── optical_system/      # Mirror mount and POB designs
│   ├── collector_mount/ # Collector mirror mount
│   ├── pob_housing/     # Projection optics box housing
│   └── mirror_mounts/   # Individual mirror mount designs (M1–M6)
├── stages/              # Stage mechanical designs
│   ├── wafer_stage/     # Wafer stage CAD and drawings
│   ├── reticle_stage/   # Reticle stage CAD and drawings
│   └── loadlock/        # Loadlock mechanism
├── vacuum/              # Vacuum system diagrams and layouts
│   ├── piping/          # P&ID diagrams
│   └── chambers/        # Chamber drawings
└── control/             # Electronics schematics
    ├── servo_amps/      # Motor drive amplifier schematics
    ├── fpga_boards/     # FPGA controller PCB designs
    └── power/           # Power distribution schematics
```

## File Formats

| Format | Tool | Purpose |
|---|---|---|
| `.FCStd` | FreeCAD (open source) | 3D CAD models |
| `.STEP` / `.STP` | Any CAD software | 3D interchange format |
| `.DXF` | LibreCAD or FreeCAD | 2D drawings |
| `.PDF` | Any viewer | Released engineering drawings |
| `.kicad_pro` | KiCad (open source) | PCB schematics |
| `.sch` / `.kicad_sch` | KiCad | Schematic files |

## Contributing Hardware Designs

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

When contributing:
1. Use open-source CAD formats (FreeCAD `.FCStd` preferred over proprietary formats).
2. Include a STEP export for interoperability.
3. Add a README in each subdirectory describing the design intent and key dimensions.
4. Reference the relevant design document in `docs/design/`.
