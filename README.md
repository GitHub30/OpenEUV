# OpenEUV — Open Source Extreme Ultraviolet (EUV) Lithography System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Research/Experimental](https://img.shields.io/badge/Status-Research%2FExperimental-blue.svg)]()

> **⚠️ Research & Educational Use Only**  
> This project is intended for academic research, simulation, and educational purposes. Building a functional EUV lithography system requires substantial resources, specialized facilities, and strict radiation/laser safety compliance. Always follow applicable regulations before attempting any hardware implementation.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Key Specifications](#key-specifications)
4. [Repository Structure](#repository-structure)
5. [Design Procedures](#design-procedures)
   - [Step 1 — EUV Light Source](#step-1--euv-light-source)
   - [Step 2 — Collector Mirror](#step-2--collector-mirror)
   - [Step 3 — Illumination System](#step-3--illumination-system)
   - [Step 4 — Reticle (Mask) Stage](#step-4--reticle-mask-stage)
   - [Step 5 — Projection Optics Box (POB)](#step-5--projection-optics-box-pob)
   - [Step 6 — Wafer Stage](#step-6--wafer-stage)
   - [Step 7 — Vacuum System](#step-7--vacuum-system)
   - [Step 8 — Metrology & Alignment](#step-8--metrology--alignment)
   - [Step 9 — Control System](#step-9--control-system)
   - [Step 10 — System Integration & Commissioning](#step-10--system-integration--commissioning)
6. [Getting Started](#getting-started)
7. [Simulation](#simulation)
8. [Bill of Materials](#bill-of-materials)
9. [Safety](#safety)
10. [Contributing](#contributing)
11. [References](#references)
12. [License](#license)

---

## Project Overview

**OpenEUV** is an open-source engineering reference for a complete **Extreme Ultraviolet (EUV) lithography system** operating at a wavelength of **13.5 nm**. The goal is to document every subsystem — from EUV plasma source to wafer stage — with enough detail that researchers, educators, and advanced hobbyists can understand, simulate, and (with appropriate resources) prototype subsystems.

EUV lithography is the technology that enables the fabrication of semiconductor nodes at 7 nm and below. It replaces conventional deep-ultraviolet (DUV) optics with all-reflective (mirror-based) optics and a plasma-based light source, because no material is transparent at 13.5 nm wavelength.

### Why Open Source?

- **Education**: Demystify the most complex manufacturing technology ever built.
- **Research**: Provide a simulation baseline for novel optical designs, resist chemistry, and control algorithms.
- **Collaboration**: Pool expertise across optics, plasma physics, mechanical engineering, vacuum technology, and software.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OpenEUV System Block Diagram                  │
│                                                                       │
│  ┌──────────────┐    ┌───────────────┐    ┌──────────────────────┐  │
│  │  Drive Laser │───▶│  EUV Source   │───▶│  Collector Mirror    │  │
│  │  (CO₂, 10µm) │    │  (LPP/DPP)   │    │  (Ellipsoidal ML)    │  │
│  └──────────────┘    └───────────────┘    └──────────┬───────────┘  │
│                                                        │              │
│                                                        ▼              │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    Vacuum Enclosure (< 1 mPa)                   │ │
│  │                                                                   │ │
│  │  ┌─────────────┐   ┌──────────────┐   ┌───────────────────────┐│ │
│  │  │ Illumination│──▶│ Reticle Stage│──▶│ Projection Optics Box ││ │
│  │  │   System    │   │  (6-axis)    │   │  (6-mirror, 0.33 NA)  ││ │
│  │  └─────────────┘   └──────────────┘   └────────────┬──────────┘│ │
│  │                                                      │           │ │
│  │                                          ┌───────────▼─────────┐│ │
│  │                                          │    Wafer Stage       ││ │
│  │                                          │  (6-DOF, nm-class)  ││ │
│  │                                          └─────────────────────┘│ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │           Control System (Real-time + Supervisory)              │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**EUV photon path**: Drive laser → tin (Sn) droplet target → plasma emits 13.5 nm EUV → collected by ellipsoidal multilayer mirror → intermediate focus → illumination system → reticle (reflective mask) → 6-mirror projection optics (4× demagnification) → wafer.

---

## Key Specifications

| Parameter | Target Value | Notes |
|---|---|---|
| EUV wavelength | 13.5 nm | Sn plasma, 2% BW |
| Source power at IF | ≥ 250 W | Intermediate Focus |
| Drive laser | CO₂, 10.6 µm, ≥ 20 kW average | Pulsed, 50 kHz rep rate |
| Collector NA | 0.20 | Ellipsoidal, Mo/Si multilayer |
| Illumination uniformity | < ±0.3% | Over 26×5 mm² slit |
| Projection NA | 0.33 | 6-mirror catoptric system |
| Demagnification | 4× | Reticle to wafer |
| Resolution | < 13 nm (half-pitch) | With PSM and OPC |
| Overlay accuracy | < 1.5 nm (3σ) | |
| Wafer throughput | ≥ 125 wph | 300 mm wafer, 80 mJ/cm² dose |
| System vacuum | < 1 × 10⁻³ Pa | EUV optical path |
| Source vacuum | < 1 × 10⁻⁴ Pa | Plasma chamber |

---

## Repository Structure

```
OpenEUV/
├── README.md                        # This file
├── LICENSE                          # MIT License
├── CONTRIBUTING.md                  # Contribution guidelines
├── docs/
│   ├── design/
│   │   ├── 01_euv_source.md         # EUV light source design
│   │   ├── 02_collector_mirror.md   # Collector mirror design
│   │   ├── 03_illumination.md       # Illumination system design
│   │   ├── 04_reticle_stage.md      # Reticle stage design
│   │   ├── 05_projection_optics.md  # Projection optics box design
│   │   ├── 06_wafer_stage.md        # Wafer stage design
│   │   ├── 07_vacuum_system.md      # Vacuum system design
│   │   ├── 08_metrology.md          # Metrology & alignment design
│   │   └── 09_control_system.md     # Control system design
│   ├── specifications/
│   │   ├── system_specs.md          # Top-level system specifications
│   │   └── optical_specs.md         # Optical prescription & tolerances
│   └── safety/
│       ├── radiation_safety.md      # EUV/X-ray radiation safety
│       └── laser_safety.md          # High-power laser safety
├── hardware/
│   ├── euv_source/                  # Source mechanical drawings & notes
│   ├── optical_system/              # Mirror mount designs
│   ├── stages/                      # Stage mechanical design
│   ├── vacuum/                      # Vacuum system diagrams
│   └── control/                     # Electronics schematics
├── software/
│   ├── control/                     # Real-time motion & process control
│   ├── simulation/                  # Optical & plasma simulation
│   └── metrology/                   # Wavefront & alignment software
├── bom/
│   └── bill_of_materials.md         # Complete BOM with vendors
└── simulations/
    └── optical/                     # Zemax/Python optical models
```

---

## Design Procedures

The following sections describe, step by step, how each subsystem is designed. Follow the steps in order because each subsystem's requirements flow down from the one before it.

---

### Step 1 — EUV Light Source

**Goal**: Generate ≥ 250 W of in-band EUV power (13.5 nm ± 1%) at the intermediate focus (IF).

#### 1.1 Source Type Selection

Two main source types are used industrially:

| Type | Principle | Pros | Cons |
|---|---|---|---|
| **LPP** (Laser-Produced Plasma) | High-power CO₂ laser ablates Sn droplets | High power, good étendue | Complex laser, Sn debris |
| **DPP** (Discharge-Produced Plasma) | Electrical discharge through Sn vapor | Simpler hardware | Lower power, erosion |

**Recommendation**: LPP with CO₂ drive laser for scalability to high power.

#### 1.2 Tin Droplet Generator Design

1. **Droplet size**: 20–30 µm diameter optimized for laser coupling efficiency.
2. **Repetition rate**: 50 kHz (one droplet per laser pulse).
3. **Velocity**: ~70 m/s (vertical downward).
4. **Generator type**: Piezo-driven orifice (Rayleigh breakup of liquid Sn jet).
5. **Material**: Tungsten or molybdenum orifice, heated to 250–300 °C (above Sn melting point 232 °C).
6. **Droplet catcher**: Below the interaction zone — liquid-cooled tungsten cone to capture unreacted Sn.

**Design procedure**:
```
a. Calculate droplet period: T = 1/f_rep = 20 µs
b. Calculate jet velocity: v_jet = d_droplet × f_rep = 25 µm × 50 kHz = 1.25 m/s
c. Orifice diameter: d_orifice ≈ 0.7 × d_droplet ≈ 17 µm
d. Driving pressure: P = 8η_Sn × v_jet × L / d_orifice² ≈ 0.5–2 bar (η_Sn ≈ 1.5 mPa·s)
e. Piezo frequency: match Rayleigh instability f_R = v_jet / (π × d_orifice) × 0.97
```

#### 1.3 CO₂ Drive Laser

| Parameter | Value |
|---|---|
| Wavelength | 10.6 µm |
| Average power | 20–40 kW |
| Pulse energy | 0.4–0.8 J |
| Pulse width | < 20 ns (pre-pulse) + 10–15 ns (main pulse) |
| Repetition rate | 50 kHz |
| Beam quality | M² < 1.3 |

**Design steps**:
1. Use a **two-pulse scheme**: A low-energy pre-pulse (3–5 mJ) vaporizes the Sn droplet into a cloud; the main pulse (≥400 mJ) irradiates the expanded cloud for higher conversion efficiency (CE).
2. Target CE ≥ 4% (EUV energy out / laser energy in into 2π sr, 13.5 nm ± 1%).
3. Focus the laser beam to a spot matching the Sn cloud diameter (~300 µm for main pulse).
4. Use a parabolic off-axis mirror (OAP) for focusing; focal length chosen to allow collector mirror clearance.

#### 1.4 Plasma Parameters

- Electron temperature: 20–30 eV (optimum for 13.5 nm emission)
- Electron density: ~10²¹ cm⁻³
- Plasma volume: ~0.5 mm³

#### 1.5 Debris Mitigation

EUV sources generate fast ions, neutrals, and micro-droplets that destroy collector mirrors:

1. **Hydrogen gas flow**: 10–100 sccm H₂ buffer gas slows Sn ions (charge exchange, thermalization). Typical pressure: 5–20 Pa in source chamber.
2. **Rotating foil trap (RFT)**: Spinning disk with radial slots that transmit EUV (photons travel straight) but intercept slow-moving debris particles.
3. **Magnetic field**: Dipole or solenoid field deflects charged Sn ions away from the collector.
4. **Collector cleaning**: Periodic in-situ H₂ plasma etching of Sn deposits on the collector surface.

See [`docs/design/01_euv_source.md`](docs/design/01_euv_source.md) for detailed calculations.

---

### Step 2 — Collector Mirror

**Goal**: Collect EUV light emitted by the plasma and form a stigmatic intermediate focus (IF) with étendue ≤ 1 mm² sr.

#### 2.1 Geometry

- **Shape**: Ellipsoidal (one focus at plasma, other focus at IF).
- **Collection solid angle**: NA_collector = 0.20 → ~0.12 sr → ~1% of 4π sr.
- **F/#**: ~1.8 (short focal length side).
- **Clear aperture**: ~600 mm diameter.
- **Central obstruction**: ~80 mm (for laser beam and droplet delivery).

#### 2.2 Multilayer Coating

EUV mirrors use **Mo/Si multilayer** coatings tuned to 13.5 nm:

```
Period thickness: d = λ / (2 × sin θ_B)  [Bragg condition]
For near-normal incidence (θ ≈ 2°): d ≈ 6.9 nm
Number of bilayers: N = 40–60 (peak reflectance ≈ 67–70%)
Mo layer thickness: 0.4d ≈ 2.8 nm
Si layer thickness: 0.6d ≈ 4.1 nm
```

**Deposition process**: Magnetron sputtering or ion beam deposition (IBD). IBD gives better layer uniformity and lower interface roughness (< 0.3 nm rms).

#### 2.3 Substrate Fabrication

1. Grind and polish a low-thermal-expansion glass-ceramic substrate (e.g., Zerodur® or ULE®, CTE < 5 ppb/K).
2. Achieve surface figure accuracy ≤ 0.1 nm rms (λ/100 at 13.5 nm).
3. Surface roughness ≤ 0.1 nm rms (to minimize EUV scatter).
4. Coat with Mo/Si multilayer using IBD.
5. Verify reflectance by EUV reflectometry at synchrotron.

#### 2.4 Thermal Management

The collector absorbs ~97% of in-band EUV (from back-scattered) and out-of-band DUV/IR radiation. Cooling channels must be machined into the substrate back surface. Target temperature stability: ±0.1 K.

See [`docs/design/02_collector_mirror.md`](docs/design/02_collector_mirror.md).

---

### Step 3 — Illumination System

**Goal**: Convert the point-source EUV beam into a homogeneous, well-controlled illumination field at the reticle plane.

#### 3.1 Optical Layout

The illumination system (ILS) consists of:

1. **Spectral purity filter (SPF)**: Transmissive grating or mirror that removes out-of-band (DUV, IR) radiation co-propagating with EUV. Typical suppression: > 10⁶ × for 193 nm DUV.
2. **Field facet mirror (FFM)**: Array of ~100–200 small mirrors that create multiple virtual sources, achieving spatial homogenization.
3. **Pupil facet mirror (PFM)**: Conjugate mirror array that maps each FFM field facet to a specific pupil point, enabling programmable illumination modes (annular, dipole, quadrupole, etc.).
4. **Grazing-incidence mirrors (optional)**: For beam steering and additional filtering.

#### 3.2 Illumination Modes

| Mode | Description | Use Case |
|---|---|---|
| Conventional | Circular pupil fill | General features |
| Annular | Ring-shaped pupil | Dense lines |
| Dipole | Two lobes | Unidirectional dense features |
| Quadrupole | Four lobes | 2D dense features |
| Freeform | Arbitrary (with digital mirror device) | Inverse lithography |

#### 3.3 Uniformity Requirements

- Slit uniformity: < ±0.3% (3σ) over 26 mm × 5 mm slit at reticle
- Telecentricity: < 0.5 mrad

#### 3.4 Design Steps

```
a. Define required slit dimensions at reticle: 26 mm × 5 mm (scanner slit)
b. Calculate required étendue: E = slit_area × sin²(NA_ill) 
   where NA_ill ≈ 0.0625 (1/4 × NA_projection)
c. Number of FFM facets: N_facet ≈ (E_source / E_facet) × efficiency
d. FFM facet size: optimize for diffraction and manufacturing (typically 1–3 mm)
e. PFM facet positions map to desired pupil fill
f. Trace rays through full ILS using Zemax/Python optics library
g. Iterate mirror tilts to achieve < ±0.3% uniformity
```

See [`docs/design/03_illumination.md`](docs/design/03_illumination.md).

---

### Step 4 — Reticle (Mask) Stage

**Goal**: Hold and scan the EUV reflective reticle with < 0.3 nm dynamic overlay error at speeds up to 1.5 m/s.

#### 4.1 Reticle Overview

EUV reticles are fundamentally different from DUV reticles:
- **Reflective** (not transmissive): All-Mo/Si multilayer mirror with absorber pattern on top.
- **Size**: 152 mm × 152 mm × 6.35 mm (SEMI standard P38).
- **Flatness**: < 50 nm peak-to-valley.
- **Absorber**: TaN or TaBN, ~70 nm thick.

#### 4.2 Stage Architecture

```
┌──────────────────────────────────────────┐
│  Reticle Masking Blade (EUV shield)      │
│  ┌────────────────────────────────────┐  │
│  │  Reticle Chuck (electrostatic)     │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │  Reticle (152×152 mm)        │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
│  Fine Stage (Lorentz actuators, 6-DOF)   │
│  Coarse Stage (linear motors, X-Y)       │
│  Metrology Frame (isolated from base)    │
└──────────────────────────────────────────┘
```

#### 4.3 Performance Requirements

| Parameter | Value |
|---|---|
| Scan velocity | 1.5 m/s |
| Acceleration | 40 m/s² |
| Scan repeatability | < 0.3 nm (3σ) |
| X-Y positioning accuracy | < 0.5 nm |
| Z/tilt (Rx, Ry) accuracy | < 1 nm / 0.1 µrad |
| Stage mass (fine) | < 5 kg |

#### 4.4 Design Steps

1. **Select motor type**: Ironless linear motors (no cogging) for X-Y coarse stage; Lorentz force voice-coil actuators for 6-DOF fine stage.
2. **Select encoder**: Laser interferometer (≥ 1 pm resolution) or planar encoder grid.
3. **Design air bearings**: For low-friction, deterministic guideway in coarse stage (or magnetic levitation).
4. **Design electrostatic chuck**: Apply 1–3 kV between chuck body and reticle back-surface to hold reticle flat.
5. **Model structural resonances**: FEA of chuck+stage assembly; first resonance ≥ 200 Hz.
6. **Control design**: Cascade PID with feedforward model for scan velocity profile; bandwidth ≥ 100 Hz.

See [`docs/design/04_reticle_stage.md`](docs/design/04_reticle_stage.md).

---

### Step 5 — Projection Optics Box (POB)

**Goal**: Demagnify the reticle pattern 4× onto the wafer with diffraction-limited imaging at NA = 0.33.

#### 5.1 Mirror Configuration

A 6-mirror (M1–M6) all-reflective optical system is used:

```
Reticle → M1 (concave) → M2 (convex) → M3 (concave) 
       → M4 (convex) → M5 (concave) → M6 (concave) → Wafer
```

- All mirrors are aspheres with Mo/Si multilayer coatings.
- System is telecentric on the image side (wafer side).
- Image field: 26 mm × 2 mm (ring-field scanner geometry).
- Demagnification: 4× (image NA = 0.33 → object NA = 0.0825).

#### 5.2 Key Optical Parameters

| Parameter | Value |
|---|---|
| NA (image side) | 0.33 |
| Wavelength | 13.5 nm |
| Diffraction limit (Rayleigh) | 13.5 nm × 0.61 / 0.33 ≈ 25 nm |
| Strehl ratio | ≥ 0.96 |
| Wavefront error (RMS) | ≤ λ/14 = 0.96 nm RMS |
| Distortion | ≤ 0.3 nm |
| Image field (ring) | 26 mm × 2 mm |
| Working distance (M6 to wafer) | ≥ 40 mm |

#### 5.3 Optical Design Steps

```python
# Pseudo-code for optical design workflow
1. Define system specifications (NA, wavelength, field, demag)
2. Select starting point (published EUV 6-mirror designs as reference)
3. Set up merit function in optical design software:
   - Minimize wavefront aberrations over all field points
   - Constrain mirror diameters (fits within POB housing)
   - Constrain chief ray angles to multilayer acceptance (< 10° from normal)
   - Enforce telecentricity at image plane
4. Run optimization (damped least squares + global search)
5. Tolerance analysis: Monte Carlo with surface figure errors,
   coating thickness errors, mirror position errors
6. Verify resolution with Hopkins transfer function / Abbe imaging
7. Output mirror prescriptions (conic constant, aspheric coefficients)
```

#### 5.4 Mirror Fabrication

For each mirror (M1–M6):

1. **Substrate**: ULE® or Zerodur® blank, precision-ground to rough aspheric shape.
2. **Ion figuring**: Ion beam figuring (IBF) to achieve surface figure < 0.1 nm rms over spatial frequencies 1–50 mm⁻¹.
3. **Metrology**: At-wavelength EUV interferometry or visible-light stitching interferometry with conversion.
4. **Multilayer deposition**: Graded Mo/Si coating (period varies across mirror aperture to compensate angle-of-incidence variation).
5. **Final verification**: EUV reflectometry, wavefront measurement.

#### 5.5 POB Structure

- **Housing material**: Invar or CFRP (low CTE).
- **Mirror mounts**: 6-DOF Invar kinematic mounts with piezo actuators for in-situ alignment.
- **Thermal control**: Isothermalized at 22.000 ± 0.001 °C.
- **Vibration isolation**: Active pneumatic isolation table supporting POB.

See [`docs/design/05_projection_optics.md`](docs/design/05_projection_optics.md).

---

### Step 6 — Wafer Stage

**Goal**: Position a 300 mm wafer with < 0.3 nm overlay accuracy at throughput ≥ 125 wph.

#### 6.1 Stage Architecture

```
┌──────────────────────────────────────────┐
│  Wafer Chuck (electrostatic, thermal)    │
│  ┌────────────────────────────────────┐  │
│  │  Wafer (300 mm)                    │  │
│  └────────────────────────────────────┘  │
│  Fine Stage (Lorentz, 6-DOF, X-Y-Z-Rx-Ry-Rz) │
│  Coarse Stage (planar motor, X-Y)        │
│  Laser interferometer metrology          │
│  Balance mass / reaction force cancel    │
└──────────────────────────────────────────┘
```

#### 6.2 Performance Requirements

| Parameter | Value |
|---|---|
| X-Y travel | 300 mm + ~50 mm |
| Scan velocity | 0.375 m/s (4× slower than reticle stage) |
| Positioning accuracy | < 0.3 nm (3σ) |
| Z-focus accuracy | < 2 nm (3σ) |
| Chuck flatness hold-down | < 50 nm |
| Temperature stability | 22.000 ± 0.010 °C |

#### 6.3 Design Steps

1. **Planar motor design**: Array of permanent magnets beneath stage; coil array in stage base; commutation by position-dependent current switching.
2. **Fine stage**: 6 Lorentz actuators (3 vertical for Z-tilt, 3 horizontal for X-Y-Rz) acting on a lightweight ceramic plate.
3. **Metrology**: Three-axis laser interferometer with Zeeman-stabilized HeNe laser (~1 pm resolution) or 2D diffraction grating encoder.
4. **Chuck design**: Electrostatic chuck with embedded PTC heaters and Peltier elements for thermal control.
5. **Focus/leveling sensor**: Air-gauge or optical triangulation sensor array to measure wafer surface height at 5–9 points before/during scan.
6. **Throughput calculation**:
   ```
   t_expose = (field_area × dose) / (slit_width × scan_vel × source_power × efficiency)
   t_step = step_settle_time + scan_overhead
   wph = 3600 / (N_fields × (t_expose + t_step) + t_wafer_exchange)
   ```

See [`docs/design/06_wafer_stage.md`](docs/design/06_wafer_stage.md).

---

### Step 7 — Vacuum System

**Goal**: Maintain EUV optical path at < 1 × 10⁻³ Pa and source region at < 1 × 10⁻⁴ Pa.

#### 7.1 Why Vacuum?

At 13.5 nm, the 1/e absorption length in air is ~50 nm (essentially zero). Even at 1 Pa, the absorption length is ~5 cm. Therefore the entire EUV optical path must be evacuated.

#### 7.2 Vacuum Zones

| Zone | Pressure | Purpose |
|---|---|---|
| Source chamber | 1 × 10⁻⁴ Pa (with H₂ buffer) | Plasma generation |
| Collector chamber | 1 × 10⁻³ Pa | Debris mitigation + EUV collection |
| ILS chamber | 5 × 10⁻⁴ Pa | Illumination optics |
| POB chamber | 1 × 10⁻⁵ Pa | Ultra-clean for mirror lifetime |
| Wafer station | 1 × 10⁻³ Pa | EUV imaging |
| Loadlock | Atmospheric ↔ 1 Pa | Wafer exchange |

#### 7.3 Pumping Strategy

```
Source chamber:   Turbomolecular pump (2000 L/s) + dry scroll roughing pump
                  + H₂ flow for debris mitigation
Optical chambers: Turbomolecular pump (500–1000 L/s each) + ionic pump
                  + cryogenic panel for hydrocarbon control
POB:              Turbomolecular pump + ionic pump + UV/ozone cleaning
Wafer station:    Turbomolecular pump + loadlock differential pumping
```

#### 7.4 Materials and Cleanliness

- All vacuum-facing surfaces: electro-polished 316L stainless steel or aluminum alloy.
- Seals: metal (CF flanges with copper or aluminum gaskets); no elastomer O-rings in high-vacuum zones.
- Hydrocarbon contamination: < 1 monolayer/day on mirrors; requires UHV-grade lubricants and bake-out at 150 °C.
- Particulate control: Class 1 cleanroom for assembly; clean-room gloves/tools only.

#### 7.5 Design Steps

1. Calculate gas load: outgassing rate × surface area + throughput from loadlock.
2. Size turbo pumps: Q_pump = S × P_target (S = pumping speed, P = pressure).
3. Design differential pumping between source and ILS (EUV-transparent aperture with turbo pump between).
4. Design foil trap (if used) to fit inside collector chamber aperture.
5. Model pressure distribution using Monte Carlo gas flow simulation (e.g., Molflow+).
6. Design bake-out system: resistive heater tape, 150 °C, 48-hour bake.

See [`docs/design/07_vacuum_system.md`](docs/design/07_vacuum_system.md).

---

### Step 8 — Metrology & Alignment

**Goal**: Measure and control the position of every optical element and the wafer surface to nanometer accuracy.

#### 8.1 Subsystems

| Subsystem | Method | Accuracy |
|---|---|---|
| Wafer stage position | Laser interferometer (3-axis) | < 0.1 nm |
| Reticle stage position | Laser interferometer (3-axis) | < 0.1 nm |
| Wafer focus/leveling | Air-gauge or confocal array | < 2 nm |
| Reticle flatness | Capacitance sensors | < 5 nm |
| Wavefront (in-situ) | Shack-Hartmann / phase-stepping | 0.05 nm rms |
| Overlay (offline) | CD-SEM / scatterometry | < 0.3 nm |
| Mirror alignment | Interferometric feedback | 0.1 nm / 0.01 µrad |

#### 8.2 Alignment Hierarchy

```
Machine frame
    └── Laser interferometer reference mirror (zerodur block)
            ├── Wafer stage metrology frame
            ├── Reticle stage metrology frame
            └── POB metrology frame
                    └── Individual mirror mounts (piezo-adjusted)
```

#### 8.3 At-Wavelength Wavefront Measurement

For EUV at 13.5 nm:

1. **Point diffraction interferometer (PDI)**: Pinhole on test mask creates a reference spherical wavefront; interfere with light through optic under test.
2. **Lateral shearing interferometer (LSI)**: Two slightly offset copies of the wavefront interfere; shear amount determines sensitivity.
3. **Hartmann sensor**: Grid of small apertures samples the wavefront; centroid shifts give local wavefront slopes.

#### 8.4 Overlay Metrology

1. Print overlay targets (box-in-box or AIM marks) on wafer.
2. Measure target offsets using CD-SEM or optical scatterometry.
3. Model overlay error as combination of translation, rotation, magnification, and higher-order terms.
4. Feed corrections back to stage control and reticle positioning.

See [`docs/design/08_metrology.md`](docs/design/08_metrology.md).

---

### Step 9 — Control System

**Goal**: Coordinate all subsystems in real time to achieve the specified throughput and accuracy.

#### 9.1 Control Hierarchy

```
Level 3 (Supervisory): Host computer — job scheduling, recipe management,
                        fault handling, data logging (Linux, Python/C++)
Level 2 (Sequence):    Real-time controller — scan sequence, interlock
                        management, subsystem coordination (RTOS, C)
Level 1 (Servo):       Axis controllers — stage servo loops, laser power
                        control, vacuum control (FPGA + DSP, C)
Level 0 (Hardware):    Sensors, actuators, amplifiers
```

#### 9.2 Motion Control

**Stage servo loop** (wafer stage example):

```
Reference     ┌──────────┐    Force      ┌───────┐   Position
trajectory ──▶│ PID + FF │──────────────▶│ Stage │──────────▶
              └──────────┘               └───────┘     │
                   ▲                                    │
                   └────────────────────────────────────┘
                          Interferometer feedback
```

- Servo bandwidth: 400 Hz (fine stage), 100 Hz (coarse stage).
- Feedforward: model-based force feedforward using Newton-Euler dynamics.
- Notch filters: at first structural resonance frequency.
- Position update rate: 50 kHz (interferometer sampling).

#### 9.3 Synchronization

- Reticle and wafer stage scan must be synchronized with ratio 4:1 (reticle velocity = 4 × wafer velocity).
- Synchronization error < 0.2 nm rms contributes directly to overlay.
- Laser pulse timing: each CO₂ pulse triggers a droplet detection event, synchronized to 50 kHz clock.
- EUV dose control: real-time power meter at IF; integrate pulse energy; adjust exposure time or scan speed.

#### 9.4 Software Stack

| Layer | Technology |
|---|---|
| Real-time servo | FPGA (Xilinx Zynq or Intel/Altera), VHDL/C |
| Motion sequencer | Beckhoff TwinCAT or custom RTOS (FreeRTOS) |
| Supervisory | Python 3.x + asyncio, or C++ |
| HMI | Qt or web-based (React + WebSocket) |
| Data pipeline | InfluxDB + Grafana for time-series monitoring |
| Recipe management | JSON/YAML + version control (Git) |

See [`docs/design/09_control_system.md`](docs/design/09_control_system.md).

---

### Step 10 — System Integration & Commissioning

#### 10.1 Integration Sequence

1. **Vacuum system qualification**: Leak check, bake-out, achieve target base pressure.
2. **Source bring-up**: Install droplet generator, bring up CO₂ laser at low power, verify droplet targeting.
3. **Collector alignment**: Align collector to maximize EUV collection; verify IF position.
4. **ILS bring-up**: Install and align FFM, PFM; measure uniformity with EUV-sensitive CCD.
5. **POB installation**: Install pre-aligned POB; align to IF using wavefront sensor.
6. **Reticle stage qualification**: Verify position accuracy with laser interferometer; measure overlay.
7. **Wafer stage qualification**: Same as reticle stage.
8. **First exposure**: Low dose, coarse alignment; print alignment marks.
9. **Full system calibration**: Grid mapping, overlay correction, focus calibration.
10. **Process qualification**: Print test patterns, measure CD and overlay, iterate.

#### 10.2 Key Acceptance Tests

| Test | Pass Criterion |
|---|---|
| EUV power at IF | ≥ 250 W |
| Illumination uniformity | < ±0.5% (initial), < ±0.3% (final) |
| Resolution (HPM) | ≤ 13 nm half-pitch on optimized process |
| Overlay (matched machine) | < 1.5 nm (3σ) |
| Wafer throughput | ≥ 125 wph at 80 mJ/cm² dose |
| Mirror lifetime | ≥ 30,000 wafers/clean (collector) |
| System availability | ≥ 90% |

---

## Getting Started

### Prerequisites

- **Simulation**: Python 3.10+, numpy, scipy, matplotlib, [rayoptics](https://github.com/mjhoptics/ray-optics) or [prysm](https://github.com/brandondube/prysm).
- **Optical design**: Zemax OpticStudio (commercial) or [OpenRayTrace](https://github.com/rfrazier716/PyRayTracer) (open source).
- **FEA**: FreeCAD + CalculiX, or Salome-Meca (open source).
- **Vacuum simulation**: [Molflow+](https://molflow.web.cern.ch/) (free, CERN).

### Running Optical Simulations

```bash
git clone https://github.com/GitHub30/OpenEUV.git
cd OpenEUV
pip install -r software/simulation/requirements.txt
python software/simulation/euv_source_model.py
python software/simulation/collector_efficiency.py
python software/simulation/projection_optics_psf.py
```

### Running Control System Simulation

```bash
python software/control/stage_servo_sim.py
```

---

## Simulation

The `simulations/` directory contains:

| File | Description |
|---|---|
| `optical/collector_model.py` | Ray-trace of collector mirror; computes collection efficiency vs. NA |
| `optical/ils_uniformity.py` | FFM/PFM ray-trace; computes slit illumination uniformity |
| `optical/projection_psf.py` | 6-mirror POB; computes PSF, Strehl, and aberrations |
| `optical/depth_of_focus.py` | Focus-exposure matrix simulation |
| `plasma/lpp_spectrum.py` | Simplified Sn LPP spectral model at 13.5 nm |

---

## Bill of Materials

See [`bom/bill_of_materials.md`](bom/bill_of_materials.md) for a detailed component list with estimated costs and vendors.

**High-level cost estimate** (research-grade prototype):

| Subsystem | Estimated Cost (USD) |
|---|---|
| CO₂ drive laser | $2M–$5M |
| EUV source (droplet gen, chamber) | $500K–$2M |
| Collector mirror | $500K–$1M |
| Projection optics (6 mirrors) | $5M–$20M |
| Stages (reticle + wafer) | $2M–$5M |
| Vacuum system | $500K–$1M |
| Control system | $500K–$1M |
| Metrology | $1M–$3M |
| Cleanroom/facility | $2M–$10M |
| **Total (rough)** | **$14M–$48M** |

> Note: Production EUV scanners (ASML NXE series) cost ~$380M each. This estimate is for a research prototype with significantly reduced throughput and yield.

---

## Safety

**EUV lithography involves significant hazards.** Read the safety documentation before attempting any hardware work:

- [`docs/safety/radiation_safety.md`](docs/safety/radiation_safety.md) — EUV photons (92 eV) and secondary X-rays.
- [`docs/safety/laser_safety.md`](docs/safety/laser_safety.md) — High-power CO₂ laser (Class 4, ≥ 20 kW).

**Summary of key safety requirements**:
- EUV radiation safety: all EUV is contained inside vacuum; no exposure outside system.
- CO₂ laser: interlocked enclosure, OD ≥ 6 eyewear for 10.6 µm, beam dump required.
- High voltage: electrostatic chucks (1–3 kV), laser power supplies (kV range).
- Tin toxicity: respiratory protection, contained disposal.
- Hydrogen gas: explosive range 4–75% in air; H₂ gas detectors, ventilation.

---

## Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

Areas where help is especially needed:
- **Optical simulation code**: Python models of ILS and POB.
- **Control system code**: Stage servo simulation, FPGA HDL.
- **Mechanical CAD**: FreeCAD models of mirror mounts, vacuum chambers.
- **Plasma physics**: Improved Sn LPP spectral and energy models.
- **Documentation**: Review and improve accuracy of design procedures.

---

## References

1. V. Bakshi (Ed.), *EUV Lithography*, 2nd ed., SPIE Press, 2018.
2. B. Wu, A. Kumar, *Extreme Ultraviolet Lithography*, McGraw-Hill, 2009.
3. H. Meiling et al., "ASML EUV program; performance update," *Proc. SPIE* 7636, 2010.
4. I. Fomenkov et al., "Light sources for high-volume manufacturing EUV lithography," *J. Phys. B*, 2018.
5. K. Ota et al., "EUV multilayer mirror design and fabrication," *Proc. SPIE* 8679, 2013.
6. H. Levinson, *Principles of Lithography*, 4th ed., SPIE Press, 2019.
7. ASML NXE:3600D specifications, [asml.com](https://www.asml.com).
8. Molflow+ documentation, [CERN](https://molflow.web.cern.ch/).
9. prysm optical simulation library, [github.com/brandondube/prysm](https://github.com/brandondube/prysm).

---

## License

MIT License — see [LICENSE](LICENSE) for details.

This project is open source and intended for educational and research use. Commercial use is permitted under the MIT license, but note that many EUV-related technologies are subject to export controls and third-party patents.
