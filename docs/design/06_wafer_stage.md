# Wafer Stage — Detailed Design

## 1. Overview

The wafer stage positions a 300 mm silicon wafer with < 0.3 nm overlay accuracy at throughput ≥ 125 wafers per hour (wph). It is the system's most performance-critical motion subsystem.

---

## 2. Stage Architecture

### 2.1 Dual-Stage Concept

Production EUV scanners use a **dual-wafer-stage** architecture:
- While one stage is under the lens (exposing), the other is loading/aligning a new wafer.
- Enables near 100% utilization of the EUV source.

For the research OpenEUV system, a single-stage design is described here.

### 2.2 Mechanical Layout

```
┌────────────────────────────────────────────────────────┐
│  Wafer (300 mm Si, 775 µm thick)                       │
│  └── Electrostatic chuck (ESC, 310 mm diameter)        │
│       └── Fine stage (6-DOF, Lorentz actuators)        │
│            └── Coarse stage (planar motor, X-Y)        │
│                 └── Granite base (isothermalized)      │
│                                                        │
│  Laser interferometer: 3 axes (X, Y, Rz)              │
│  Focus/leveling sensor: 5-point optical triangulation  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Coarse Stage (Planar Motor)

### 3.1 Principle

A planar (flat) motor consists of a 2D array of coils in the stator (base) and a 2D array of permanent magnets on the mover (stage bottom). By commutating current through the coils, force can be generated in X and Y independently.

### 3.2 Parameters

| Parameter | Value |
|---|---|
| Travel (X × Y) | 400 mm × 400 mm |
| Peak force (X or Y) | 1500 N |
| Continuous force | 400 N |
| Maximum velocity | 0.5 m/s |
| Maximum acceleration | 30 m/s² |
| Stage mass | ~20 kg |
| Coil pitch | 20 mm |
| Magnet pitch | 10 mm |

### 3.3 Commutation

The coil current pattern is updated in real time as a function of measured stage position to maintain consistent force direction and magnitude (sinusoidal commutation). FPGA handles current switching at 100 kHz update rate.

---

## 4. Fine Stage (Lorentz Actuators)

### 4.1 Configuration

- **6 Lorentz (voice-coil) actuators**: 3 horizontal (X, Y, Rz), 3 vertical (Z, Rx, Ry).
- The fine stage plate floats within ±2 mm of the coarse stage center in X/Y, and ±0.5 mm in Z.
- The coarse stage follows the fine stage with ~10 µm lag (coarse stage does gross positioning, fine stage does nanometer-level correction).

### 4.2 Parameters

| Parameter | Value |
|---|---|
| Fine stage mass | 8 kg |
| Fine stage material | SiC (low mass, high stiffness) |
| Lorentz force constant | 15 N/A |
| Max current | ±5 A per axis |
| Peak force | ±75 N per axis |
| X/Y stroke | ±3 mm |
| Z stroke | ±0.5 mm |
| First resonance | ≥ 150 Hz |

---

## 5. Electrostatic Chuck

### 5.1 Requirements

- Clamp 300 mm wafer flat: back-surface flatness correction to achieve front-surface ≤ 50 nm non-flatness.
- Temperature control: 22.000 ± 0.005°C.
- Contact force: uniform across wafer (minimize bowing-induced stress in wafer).

### 5.2 Design

- **Chuck material**: AlN (aluminum nitride) — high thermal conductivity (180 W/m·K), low CTE mismatch with Si.
- **Electrode pattern**: Tripole (3-zone) for uniform clamping force.
- **Operating voltage**: 500–1500 V.
- **Backside gas**: He at 500–1000 Pa between wafer and chuck for thermal conduction.
- **Protrusion mesas**: 0.5 mm diameter, 20 µm height, at ~4 mm pitch (to define wafer contact plane and minimize particle contact area).
- **Embedded heaters**: Resistive elements in AlN, ±0.5 W control resolution per zone.
- **Temperature sensors**: 4 × Pt100 RTD, ±0.01 K resolution.

---

## 6. Focus and Leveling

### 6.1 Purpose

EUV has an extremely narrow depth of focus (±62 nm at NA = 0.33). The wafer surface must be measured and adjusted to land within ±30 nm of the best focal plane during every scan.

### 6.2 Sensor Design

- **Type**: Multi-point air gauge or confocal optical sensor array.
- **Points**: 9 measurement points arranged in 3×3 grid, spaced 10 mm apart.
- **Measurement range**: ±0.5 mm (capture range), ±5 µm (precision range).
- **Precision**: < 1 nm rms (in precision range).
- **Update rate**: 10 kHz.

### 6.3 Operation

Before each die scan:
1. Measure wafer height map at 9 points.
2. Fit a plane (Z, Rx, Ry) to minimize least-squares deviation.
3. Command fine stage Z, Rx, Ry to position wafer in focal plane.
4. During scan: use pre-measured height map for feedforward Z correction.

---

## 7. Laser Interferometer Metrology

### 7.1 System

- **Laser**: Zeeman-stabilized HeNe (632.8 nm), frequency stability ≤ 5 × 10⁻⁹.
- **Axes**: 3 beams for X, Y, Rz (1 pm resolution).
- **Reference mirror**: Zerodur® flat mirror, λ/20 flatness, mounted on metrology frame.
- **Beam splitter**: Non-polarizing (to avoid polarization-dependent pointing errors).

### 7.2 Environmental Compensation

The laser interferometer reads the optical path length in air. Variations in air temperature, pressure, and humidity change the refractive index and introduce measurement errors:

```
Air refractive index (Edlén equation, simplified):
n - 1 ≈ 2.82 × 10⁻⁷ × P / T  (P in Pa, T in K)

Sensitivity:
dn/dT ≈ -1 × 10⁻⁶ /K → 1 nm error per 1 mm path per K temperature change
dn/dP ≈ +2.7 × 10⁻⁹ /Pa → 1 nm error per 1 mm path per 370 Pa pressure change
```

Compensation methods:
1. Use vacuum-path interferometer (no air in beam path) — best.
2. Measure air properties in real time (Barometric pressure, temperature) and apply Edlén correction.
3. Vacuum enclosure for beam paths (preferred for wafer stage).

---

## 8. Throughput Analysis

### 8.1 Exposure Time per Field

```
Wafer exposure parameters:
    Field size: 26 mm × 33 mm (typical die)
    EUV dose required: 80 mJ/cm²
    Slit width at wafer: 26 mm × 2 mm

Slit area: 26 × 2 = 52 mm² = 0.52 cm²
EUV power at wafer: P_wafer (to be measured)
    = Source power × ILS transmission × POB transmission × resist efficiency
    ≈ 250 W × 13.7% × (0.67)⁶ (6 POB mirrors) × 0.9
    = 250 × 0.137 × 0.090 × 0.9 = 2.78 W  (too low)

Revised with corrected POB transmission:
    POB transmission = product of reflectances: 0.67⁶ ≈ 9.0% → low
    Peak EUV power at wafer ≈ 2–5 W (strongly dependent on all losses)

Scan velocity to achieve 80 mJ/cm² dose:
    v_scan = P_wafer / (dose × slit_width)
    = 3 W / (80 × 10⁻³ J/cm² × 2.6 cm)
    = 3 / 0.208 = 14.4 cm/s = 0.144 m/s

Time to scan 33 mm field:
    t_scan = 33 mm / 144 mm/s = 0.23 s

Step time (settle + load): ~0.1 s
Fields per 300 mm wafer: ~80 (26×33 mm dies)

Cycle time: 80 × (0.23 + 0.10) + 60 s (load/unload) = 86.4 s
Throughput: 3600 / 86.4 ≈ 41 wph (research system)
```

Note: Production systems achieve 125–170 wph with 250+ W source power, shorter settle times, and dual-stage architecture.

---

## 9. References

1. H. Butler, "Position control in lithographic equipment," *IEEE Control Syst. Mag.* 31, 2011.
2. J. Compter, "Electro-dynamic planar motor," *Proc. SPIE* 4902, 2002.
3. I. Kim, "Precision six-DOF motion control using Lorentz actuators," *Mechatronics* 24, 2014.
4. V. Bakshi (Ed.), *EUV Lithography*, 2nd ed., SPIE Press, 2018, Ch. 8.
