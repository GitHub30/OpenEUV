# Metrology and Alignment — Detailed Design

## 1. Overview

EUV lithography at sub-10 nm resolution requires position measurement and control at the single-nanometer level. This document describes the metrology systems for stage position, wavefront measurement, focus/leveling, and overlay.

---

## 2. Stage Position Metrology

### 2.1 Laser Interferometry Principle

A Zeeman-split HeNe laser produces two closely spaced optical frequencies (f₁ and f₂, split by ~2 MHz). When one beam reflects off a moving mirror, the Doppler shift ∆f is proportional to velocity. Integration gives displacement:

```
∆x = (λ/2) × ∫(f₁ - f₂) dt / f_reference

Resolution: λ / (2 × interpolation factor)
For 10,000× interpolation: 632.8 nm / 20,000 ≈ 0.032 nm → 32 pm resolution
```

### 2.2 Axis Configuration

For the wafer stage (3-axis):

```
                    Y-beam (along Y axis)
                         │
                         │   Reference mirror (flat, λ/20)
X-beam ─────────────────▶│◀── X-beam
                         │
                         ▼
                    Rz = (X_right - X_left) / d_beam_separation
```

- **X axis**: 2 parallel X-beams separated by distance d_Y → measures X and Rz.
- **Y axis**: 1 Y-beam → measures Y.
- **Total**: 3 interferometer channels → X, Y, Rz (full in-plane position).

For Z, Rx, Ry: capacitance sensors or optical triangulation (shorter range, but sub-nm for Z-focus).

### 2.3 Thermal and Environmental Correction

Environmental perturbations cause refractive index changes in the laser path:

```
Compensation algorithm:
1. Measure T_air (Pt100, resolution 0.001°C), P_atm (barometer, resolution 1 Pa)
2. Compute n_air from Edlén equation
3. Correct measured position: x_corrected = x_raw × (n_vacuum / n_air)
                               n_vacuum = 1.000000 (reference)
4. Residual error after compensation: < 0.1 nm per meter of beam path
```

### 2.4 Deadpath Compensation

Any unequal path length between beam splitter and reference mirror introduces a length error proportional to environmental changes. Design for minimum deadpath:
```
Deadpath < 50 mm → error < 0.1 nm / m × 0.05 m × δn_air < 0.005 nm/K → negligible
```

---

## 3. Wafer Focus and Leveling

### 3.1 Optical Triangulation Sensor

- **Type**: Laser triangulation (confocal or astigmatic detection).
- **Measurement point**: 5–9 points on wafer surface, 10–15 mm spacing.
- **Working distance**: 40–60 mm (below M6 mirror exit).
- **Range**: ±0.5 mm (capture), ±5 µm (precision range).
- **Resolution**: < 1 nm rms.
- **Update rate**: 10 kHz.

### 3.2 Height Map Generation

Before each wafer scan:
1. Move wafer stage to sample all 9 measurement points across die field.
2. Fit a 2D plane (Z, Rx, Ry) and a higher-order surface to the 9-point map.
3. Generate a height correction profile for the scan trajectory.

### 3.3 Air Gauge (Alternative)

For higher precision (< 0.5 nm), differential air gauges can measure wafer height:
```
Principle: High-pressure air jets impinge on wafer surface; back-pressure is
proportional to gap height. Differential measurement of two jets eliminates
common-mode errors.
Resolution: ~0.1 nm with precision pressure transducer.
```

---

## 4. Reticle Flatness Measurement

### 4.1 Capacitance Sensor Array

- **Sensors**: 4–8 non-contact capacitance sensors surrounding the reticle chuck.
- **Resolution**: < 5 nm.
- **Measurement**: Backside of reticle relative to chuck face.
- **Function**: Verify reticle is properly clamped; detect particulates causing bump.

### 4.2 In-Situ EUV Wavefront Impact

Reticle non-flatness causes field-dependent focus and magnification errors. A 50 nm bump on the reticle causes:
```
Focus error at wafer = 50 nm / 4² = 3.1 nm  (due to 4× demagnification)
→ acceptable if ≤ DOF/2 = 31 nm
Magnification error: δM = (n-1) × δz / z_pupil  [small amount]
```

---

## 5. At-Wavelength Wavefront Measurement

Visible-light interferometry cannot be used directly for EUV mirror characterization because the wavefront must be measured at 13.5 nm to include all wavelength-dependent effects (multilayer phase shifts, coating thickness variations).

### 5.1 Point Diffraction Interferometer (PDI)

```
Layout:
    EUV source → test optic (under test) → test mask
                          ↕                        ↕
                    signal wavefront         reference wavefront
                    (through optic)         (from pinhole diffraction)
    → interference pattern on EUV CCD → wavefront reconstruction
```

The test mask has:
- A window transmitting the signal beam (through the optic).
- A pinhole (< λ_EUV / (2 NA)) creating a diffraction-limited reference spherical wave.

**Wavefront measurement accuracy**: < 0.05 nm rms if pinhole is < 0.5 × (λ/NA).

### 5.2 Lateral Shearing Interferometer (LSI)

A diffraction grating placed in the beam creates two sheared copies of the wavefront. The interference pattern gives the wavefront derivative, which can be integrated to recover the wavefront.

```
Shear: s = λ × d / (Λ × NA)  where Λ = grating period, d = grating-to-detector distance
Sensitivity: ∆φ = 2π × (δW/δx) × s / λ
```

### 5.3 In-Situ Hartmann Sensor

For routine monitoring during exposure:
- A small Hartmann screen (array of 100–200 apertures) is placed in the EUV beam path.
- An EUV CCD detector downstream records the spot pattern.
- Centroid shifts of spots give local wavefront slopes.
- Zernike coefficients are computed in real time.
- Mirror actuators are commanded to correct wavefront.

---

## 6. Overlay Metrology

### 6.1 Definition

Overlay is the misalignment between two layers of a multi-layer IC process. Overlay error budget:

```
Total overlay (3σ) = RSS(scanner contribution, process contribution, measurement contribution)
Target: < 1.5 nm (3σ) total
Scanner contribution budget: < 1.0 nm (3σ)
```

### 6.2 Overlay Targets

Standard overlay targets for EUV:
- **Box-in-box (BiB)**: Outer box in layer N-1, inner box in layer N; measure offset.
- **AIM (Advanced Imaging Metrology) marks**: Periodic gratings, measured by scatterometry.
- **NILS-based targets**: Near-threshold patterns for maximum sensitivity.

### 6.3 Measurement Equipment

| Instrument | Method | Accuracy | Use |
|---|---|---|---|
| CD-SEM | Electron beam imaging | 0.1–0.3 nm | Lab/process development |
| Optical overlay tool | Brightfield microscopy | 0.5–1 nm | In-line production |
| Scatterometry (OCD) | Diffraction modeling | 0.2–0.5 nm | In-line production |

### 6.4 Overlay Error Decomposition

Measured overlay errors are decomposed into:
```
OVL(x,y) = T_x + T_y·(y/R) + T_Rz·(x²+y²)^0.5/R + M_x·x + M_y·y
           + asymmetric terms (higher order)
where:
    T_x, T_y = translation
    T_Rz = rotation
    M_x, M_y = magnification
    R = wafer radius = 150 mm
```

Corrections are fed back to:
- Stage position offsets (for T_x, T_y, T_Rz).
- Lens distortion correction (for M_x, M_y via mirror actuators or stage correction tables).

---

## 7. Alignment System

### 7.1 Wafer Alignment

Before exposure, alignment marks pre-printed on the wafer are located:

1. **Global alignment**: Coarse wafer position from 2 alignment marks; determine translation + rotation.
2. **Enhanced Global Alignment (EGA)**: Measure 8–16 marks; fit grid model (translation, rotation, scale, non-orthogonality); correct systematic wafer-level distortions.
3. **Die-by-die alignment**: Measure marks on each die (slower, used for high-accuracy layers only).

**Alignment sensor**: Off-axis optical alignment sensor (wavelength 633 nm or 488 nm, outside EUV beam path); through-the-lens (TTL) alignment preferred.

### 7.2 Reticle Alignment

1. Load reticle; measure reticle mark positions with reticle alignment camera.
2. Correct for reticle placement error (translation ≤ 10 µm, rotation ≤ 100 µrad) using fine stage.
3. Use reticle interferometer for continuous position monitoring during scan.

---

## 8. References

1. M. Terry, "Interferometric measurement of stage position," *Proc. SPIE* 4688, 2002.
2. P. Dirksen et al., "Assessment of an extended Nijboer-Zernike approach to the merit function," *J. Micro/Nanolithogr.* 7, 2008.
3. J. Kirk, "Measurement of EUV wavefront aberrations using a Hartmann sensor," *Proc. SPIE* 6151, 2006.
4. H. Levinson, *Principles of Lithography*, 4th ed., SPIE Press, 2019, Ch. 6.
5. C. Fischle et al., "EUV overlay measurement with scatterometry," *Proc. SPIE* 10145, 2017.
