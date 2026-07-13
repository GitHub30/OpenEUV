# System Specifications

## 1. Top-Level Requirements

| Requirement | Value | Rationale |
|---|---|---|
| Technology node target | ≤ 3 nm (research); ≤ 7 nm (initial) | Future-proof design |
| Resolution (half-pitch) | ≤ 13 nm (with OPC/PSM) | k₁ = 0.32, NA = 0.33 |
| Depth of focus | ± 60 nm | NA = 0.33, λ = 13.5 nm |
| Overlay accuracy | < 1.5 nm (3σ) | Mixed-and-match budget |
| CD uniformity | < 1% (3σ) | Across 26×33 mm die |
| Wafer throughput | ≥ 125 wph (production target) | 80 mJ/cm², 300 mm wafer |
| System availability | ≥ 90% | Scheduled maintenance excluded |
| Mean time between failures (MTBF) | ≥ 1000 h | For research prototype |
| Footprint | < 10 m × 6 m | Cleanroom bay |

---

## 2. EUV Source Specifications

| Parameter | Value |
|---|---|
| EUV wavelength | 13.5 nm |
| Bandwidth | ±1% (2% total) |
| EUV power at IF | ≥ 250 W |
| Source étendue | ≤ 1.0 mm² sr |
| Drive laser wavelength | 10.6 µm (CO₂) |
| Drive laser average power | 20–40 kW |
| Pulse repetition rate | 50 kHz |
| Conversion efficiency (CE) | ≥ 4% |
| Collector lifetime | ≥ 30,000 wafer equivalent exposures |

---

## 3. Illumination System Specifications

| Parameter | Value |
|---|---|
| Slit dimensions at reticle | 26 mm × 5 mm |
| Dose uniformity (slit) | < ±0.3% (3σ) |
| Telecentricity error | < 0.5 mrad |
| Illumination modes | Conventional, annular, dipole, quadrupole |
| σ outer (conventional) | 0.80 |
| σ inner (annular) | 0.60 |
| ILS total EUV transmission | ≥ 13% |

---

## 4. Projection Optics Specifications

| Parameter | Value |
|---|---|
| Image-side NA | 0.33 |
| Object-side NA | 0.0825 |
| Demagnification | 4× |
| Wavelength | 13.5 nm |
| Image field | 26 mm × 2 mm (ring field) |
| Wavefront error (RMS) | ≤ 0.96 nm (λ/14) |
| Strehl ratio | ≥ 0.96 |
| Distortion | ≤ 0.3 nm |
| Flare (EUV scatter) | ≤ 5% |
| POB EUV transmission | ~9% (6 mirrors × 67% each) |

---

## 5. Reticle Stage Specifications

| Parameter | Value |
|---|---|
| Reticle format | 152 mm × 152 mm × 6.35 mm |
| Scan velocity | 1.5 m/s |
| Max acceleration | 40 m/s² |
| Scan repeatability | < 0.3 nm (3σ) |
| In-plane position accuracy | < 0.5 nm |
| Z, tilt accuracy | < 1 nm / 0.1 µrad |

---

## 6. Wafer Stage Specifications

| Parameter | Value |
|---|---|
| Wafer size | 300 mm (200 mm optional) |
| Scan velocity | 0.375 m/s |
| Max acceleration | 20 m/s² |
| Position accuracy | < 0.3 nm (3σ) |
| Z focus accuracy | < 2 nm (3σ) |
| Chuck temperature stability | ±0.010°C |

---

## 7. Vacuum Specifications

| Zone | Base Pressure | Operating Pressure |
|---|---|---|
| Source chamber | 10⁻⁶ Pa | 5–20 Pa (H₂) |
| Optical chambers | 10⁻⁵ Pa | 10⁻³ Pa |
| POB | 10⁻⁶ Pa | 10⁻⁵ Pa |
| Loadlock cycle time | — | < 60 s |

---

## 8. Environmental Requirements

| Parameter | Value |
|---|---|
| Cleanroom class | ISO Class 3 (Class 1 at reticle/wafer handling) |
| Temperature | 22.0 ± 0.1°C (room), 22.000 ± 0.001°C (POB) |
| Humidity | 45 ± 5% RH |
| Floor vibration | VC-E or better (< 3 µm/s at 1–80 Hz) |
| Acoustic noise | < 65 dBA |
| Seismic isolation | > 30 dB at 1–100 Hz |
| Power supply | 480 V 3-phase, 200 kVA |
| Cooling water | UPW at 22°C, 500 L/min |
| N₂ supply | 200 SLPM at 6 bar |
| Compressed dry air | 200 SLPM at 7 bar |
| H₂ supply | 10 SLPM at 3 bar |
