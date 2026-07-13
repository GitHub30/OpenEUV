# Projection Optics Box (POB) — Detailed Design

## 1. Overview

The Projection Optics Box (POB) is the heart of the EUV lithography system. It demagnifies the reticle pattern 4× onto the wafer surface using a 6-mirror all-reflective optical system. It must achieve diffraction-limited imaging at NA = 0.33 with wavefront error ≤ λ/14 rms (0.96 nm) across a 26 mm × 2 mm ring-field image.

---

## 2. Design Constraints

### 2.1 Why Reflective Optics?

At 13.5 nm, no material has useful transmission (all transmit < 0.01% for > 1 µm thickness). Therefore, all optical elements must be mirrors.

### 2.2 Why Ring-Field?

A circular mirror can only image a ring-shaped field without severe off-axis aberrations (particularly distortion and field curvature). The 26 mm × 2 mm slit is positioned on such a ring (radius ~30 mm from optical axis). The wafer is exposed by scanning through this slit.

### 2.3 Why 6 Mirrors?

- An even number of mirrors is needed so the image has the same orientation as the object (no parity flip).
- 4 mirrors: achievable at NA ≤ 0.25.
- 6 mirrors: enables NA = 0.33 with sufficient degrees of freedom to correct aberrations.
- 8 mirrors: enables NA = 0.55 (High-NA EUV), under development.

---

## 3. Optical Design (6-Mirror System)

### 3.1 Mirror Configuration

```
                    Reticle (object)
                          │
                         M1 (concave, large, near pupil)
                          │
                         M2 (convex, small)
                          │
                         M3 (concave, medium)
                          │
                         M4 (convex, medium)
                          │
                         M5 (concave, large)
                          │
                         M6 (concave, large, near image)
                          │
                       Wafer (image)
```

### 3.2 Mirror Parameters (Nominal 0.33 NA Design)

| Mirror | Type | Approximate Diameter | Role |
|---|---|---|---|
| M1 | Concave asphere | 800 mm | Primary collimating |
| M2 | Convex asphere | 200 mm | Field correction |
| M3 | Concave asphere | 400 mm | Pupil relay |
| M4 | Convex asphere | 150 mm | Field flattening |
| M5 | Concave asphere | 700 mm | Near-pupil correction |
| M6 | Concave asphere | 600 mm | Final imaging |

All mirrors are aspheres described by:
```
z(r) = r² / (R(1 + √(1 - (1+K)r²/R²))) + A₄r⁴ + A₆r⁶ + A₈r⁸ + A₁₀r¹⁰ + ...
where:
    R = vertex radius of curvature
    K = conic constant
    A₄, A₆, ... = higher-order aspheric coefficients
```

### 3.3 System Specifications

| Parameter | Value |
|---|---|
| Wavelength | 13.5 nm |
| Numerical aperture (image side) | 0.33 |
| Numerical aperture (object side) | 0.0825 (= NA/4) |
| Magnification | -0.25 (4× reduction) |
| Image field | 26 mm × 2 mm (ring field, radius ≈ 30 mm) |
| Object field | 104 mm × 8 mm (ring field) |
| Telecentricity | Image side telecentric (chief ray ⊥ wafer) |
| Working distance (M6 to wafer) | ≥ 40 mm |
| Track length (reticle to wafer) | ~1400 mm |
| Wavefront error | ≤ 0.96 nm rms (λ/14) |
| Strehl ratio | ≥ 0.96 |
| Distortion | ≤ 0.3 nm |
| Flare (stray EUV light) | ≤ 5% |

---

## 4. Aberration Budget

### 4.1 Zernike Decomposition

Wavefront error is described by Zernike polynomials Z_n^m(ρ,φ):

| Zernike Term | Name | Tolerance (nm rms) |
|---|---|---|
| Z4 | Defocus | 0.20 |
| Z5, Z6 | Astigmatism | 0.15 |
| Z7, Z8 | Coma | 0.10 |
| Z9 | Spherical | 0.15 |
| Z10–Z16 | Higher order | 0.30 (total) |
| Z17–Z36 | High order | 0.20 (total) |
| **Total RSS** | | **≤ 0.50 nm rms** |

(Budget allows additional 0.46 nm for manufacturing and alignment errors to reach ≤ 0.96 nm total.)

### 4.2 Imaging Performance

```
Rayleigh resolution: R = 0.61 λ / NA = 0.61 × 13.5 / 0.33 = 25.0 nm
Depth of focus (Rayleigh): DOF = ± λ / (2 NA²) = ± 62 nm
k₁ factor (practical): k₁ = HP × NA / λ
    For 13 nm HP: k₁ = 13 × 0.33 / 13.5 = 0.32 (with OPC/PSM)
```

---

## 5. Mirror Fabrication

### 5.1 Surface Figure Requirements

| Mirror | Diameter | Figure rms | Roughness rms |
|---|---|---|---|
| M1 | 800 mm | ≤ 0.08 nm | ≤ 0.10 nm |
| M2 | 200 mm | ≤ 0.08 nm | ≤ 0.10 nm |
| M3 | 400 mm | ≤ 0.08 nm | ≤ 0.10 nm |
| M4 | 150 mm | ≤ 0.10 nm | ≤ 0.10 nm |
| M5 | 700 mm | ≤ 0.08 nm | ≤ 0.10 nm |
| M6 | 600 mm | ≤ 0.08 nm | ≤ 0.10 nm |

### 5.2 Fabrication Process

For each mirror:

1. **Blank procurement**: ULE® or Zerodur® blank.
2. **CNC grinding**: Rough aspheric shape, ±5 µm figure error.
3. **MRF (Magnetorheological Finishing)**: Reduce figure error to ~1 nm rms.
4. **IBF (Ion Beam Figuring)**: Final figuring to ≤ 0.1 nm rms.
5. **Metrology**: Stitching phase-shifting interferometry (PSI) with computer-generated hologram (CGH) null lens for asphere verification.
6. **Mo/Si Multilayer Deposition**: Graded period IBD coating.
7. **At-wavelength verification**: EUV Hartmann wavefront sensor at synchrotron.

### 5.3 Mirror Cleanliness

EUV irradiation of contaminated mirror surfaces causes carbon growth (polymerization of hydrocarbon molecules). Requirements:
- Carbon contamination rate: < 0.01 nm/day at operating dose.
- Hydrocarbon partial pressure: < 10⁻⁸ Pa in POB.
- In-situ cleaning: UV/ozone or atomic hydrogen, or periodic replacement of mirror coatings.

---

## 6. POB Structure

### 6.1 Housing

- **Material**: CFRP (carbon fiber reinforced polymer) tubes and ribs, or Invar 36 castings.
- **CTE requirement**: < 1 ppm/K for housing structure.
- **Stiffness**: First structural resonance ≥ 80 Hz.
- **Size**: ~1.8 m × 0.8 m × 0.8 m.

### 6.2 Mirror Mounts

Each mirror mount must:
- Position the mirror in 6-DOF to within ±0.1 nm (translation) and ±0.01 µrad (rotation) of nominal.
- Include piezo actuators for in-situ fine alignment (6-DOF per mirror).
- Provide stable, repeatable positioning after thermal cycling.

**Mount type**: Kinematic 3-point contact with flexure blades. Piezo stacks in-line with flexures for nanometer adjustment.

### 6.3 Thermal Control

The POB must be isothermalized to prevent thermally induced figure changes:

- **Target temperature**: 22.000°C.
- **Stability**: ±0.001°C (1 mK).
- **Method**: Forced gas circulation (N₂) through temperature-controlled heat exchanger; each mirror mount has embedded temperature sensor and heater.
- **Heating due to EUV absorption**: ~0.1–1 W per mirror (3% absorption of reflected light + scatter).

---

## 7. Alignment Procedure

### 7.1 Initial Alignment (ex-situ)

1. Install M6 and align to wafer plane reference using visible-light interferometry.
2. Add M5, align using interferometer from image side.
3. Continue adding M4, M3, M2, M1 from image toward object side.
4. Use computer-generated hologram (CGH) test plates for each asphere stage.
5. Final system wavefront measurement with point-diffraction interferometer (PDI).

### 7.2 In-Situ Alignment

1. Print alignment patterns on a test wafer using known-good EUV process.
2. Measure wavefront using in-situ Hartmann sensor.
3. Compute required mirror tilt/shift corrections (sensitivity matrix inversion).
4. Apply corrections via piezo actuators.
5. Iterate until wavefront ≤ 0.5 nm rms.

---

## 8. Stray Light (Flare)

EUV scattered by mirror roughness, dust, and multilayer imperfections creates a diffuse background (flare) that reduces image contrast:

```
Flare ≈ (4π σ_rms / λ)² × cos θ_i × (angular scattering function)
For σ_rms = 0.1 nm, λ = 13.5 nm:
    TIS (total integrated scatter per mirror) = (4π × 0.1 / 13.5)² ≈ 8.7 × 10⁻³ = 0.87%
    For 6 mirrors: flare ≈ 1 - (1 - 0.0087)⁶ ≈ 5.1%  ← at the budget limit
```

Flare mitigation: keep roughness < 0.1 nm rms, keep POB pressure < 10⁻⁵ Pa to prevent carbon growth.

---

## 9. References

1. D. Williamson, "The elusive diffraction limit," *Proc. SPIE* 3048, 1997.
2. T. Jewell et al., "23.9 nm, 0.7 NA, EUV optical system," *Proc. SPIE* 10583, 2018.
3. J. Benschop et al., "EUV lithography: present and future," *Proc. SPIE* 6921, 2008.
4. K. Murakami et al., "Development of EUV projection optics," *Proc. SPIE* 7636, 2010.
5. V. Bakshi (Ed.), *EUV Lithography*, 2nd ed., SPIE Press, 2018, Ch. 7.
