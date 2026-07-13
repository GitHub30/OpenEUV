# Collector Mirror — Detailed Design

## 1. Overview

The collector mirror collects EUV radiation emitted by the LPP source and focuses it to the intermediate focus (IF). It is the first optical element in the system and the most exposed to debris. Its reflectance, collection solid angle, and lifetime directly determine the EUV power budget.

---

## 2. Optical Design

### 2.1 Shape

An **ellipsoid of revolution** is used:
- One focus coincides with the plasma interaction point (source point).
- Other focus is the intermediate focus (IF), which feeds the illumination system.
- The ellipsoid provides stigmatic imaging of the source point to the IF.

```
Ellipse parameters:
    a = semi-major axis
    b = semi-minor axis
    c = focal distance (c² = a² - b²)

Source at (-c, 0), IF at (+c, 0)
Collection angle: θ_max = arcsin(NA_coll) measured from source side
```

### 2.2 Parameters

| Parameter | Value |
|---|---|
| Source-to-collector vertex distance | ~100 mm |
| Collector-to-IF distance | ~1600 mm |
| Semi-major axis a | ~850 mm |
| Semi-minor axis b | ~400 mm |
| Collection NA (at source) | 0.20 |
| Maximum collection angle θ_max | ~60° half-angle (from optical axis) |
| Clear aperture | ~600 mm diameter |
| Central obstruction (laser/droplet entry) | ~80 mm diameter |
| EUV reflectance (Mo/Si peak) | ~67% |

### 2.3 Collection Efficiency

```
Solid angle collected:
    Ω = 2π × (1 - cos θ_max)      [sr]
    For θ_max = 60°: Ω = 2π(1 - 0.5) = π sr ≈ 3.14 sr

Fraction of 4π sr:
    f = Ω / (4π) = 1/4 = 25%

Note: Central obstruction reduces this:
    Ω_obs = 2π(1 - cos θ_min)  where θ_min = arctan(40/100) ≈ 21.8°
    f_net = (Ω - Ω_obs) / (4π) ≈ (3.14 - 0.42) / 12.57 ≈ 21.6%

After one reflection (67% reflectance):
    Net EUV throughput to IF ≈ 21.6% × 67% ≈ 14.5%
```

---

## 3. Multilayer Coating Design

### 3.1 Mo/Si Multilayer Principle

At 13.5 nm, no material is transparent. Reflection is achieved using Bragg interference in a periodic multilayer stack. Mo absorbs less than Si at 13.5 nm, so Mo/Si is used.

**Bragg condition:**
```
2d × sin θ_B = mλ
where:
    d = bilayer period thickness
    θ_B = Bragg angle (from surface)
    m = diffraction order (m=1)
    λ = 13.5 nm

For near-normal incidence (θ_B ≈ 88°, grazing = 2°):
    d ≈ λ / (2 × sin θ_B) ≈ 13.5 / (2 × 1.0) ≈ 6.9 nm
```

### 3.2 Layer Stack Parameters

| Parameter | Value |
|---|---|
| Bilayer period d | 6.9 nm |
| Mo layer thickness | 0.4d = 2.76 nm |
| Si layer thickness | 0.6d = 4.14 nm |
| Number of bilayers N | 40–60 |
| Peak reflectance (13.5 nm, near-normal) | 67–70% |
| Reflectance bandwidth (FWHM) | ~0.5 nm |
| Angular acceptance (FWHM) | ~10° |

### 3.3 Graded Coating

The collector spans a large range of incidence angles (~2° to ~60°). To maintain high reflectance across this range, the bilayer period must be graded:

```
d(θ) = λ / (2 × sin θ_local)

At θ = 2° (near-normal): d = 6.9 nm
At θ = 20°: d = 13.5 / (2 × sin 20°) = 13.5 / 0.684 = 19.7 nm
At θ = 45°: d = 13.5 / (2 × sin 45°) = 9.55 nm
At θ = 60°: d = 13.5 / (2 × sin 60°) = 7.79 nm
```

The deposition system must vary the period thickness across the 600 mm aperture during coating.

### 3.4 Deposition Process

**Ion Beam Deposition (IBD)**:
1. Load substrate into UHV deposition chamber (base pressure < 10⁻⁷ Pa).
2. Clean substrate surface with low-energy Ar ion beam (50–100 eV, 5 min).
3. Deposit Mo layer: Mo target, 1.0 keV Ar ion beam, rate ~0.1 nm/s.
4. Deposit Si layer: Si target, 1.0 keV Ar ion beam, rate ~0.1 nm/s.
5. Repeat for N bilayers with programmed planetary motion for graded coating.
6. Cap layer: Si (prevents Mo oxidation), or Si₃N₄ for chemical stability.

**Quality control**:
- Measure period by X-ray reflectometry (XRR) on witness samples.
- Measure peak reflectance on witness samples at EUV synchrotron beamline.
- Measure thickness map by visible-light ellipsometry.

---

## 4. Substrate Fabrication

### 4.1 Material Selection

| Material | CTE (ppb/K) | Young's modulus (GPa) | Notes |
|---|---|---|---|
| Zerodur® (Schott) | 0 ± 10 | 91 | Preferred for metrology stability |
| ULE® (Corning) | 0 ± 30 | 67.6 | Slightly less stiff |
| Silicon carbide (CVD) | 2400 | 466 | Very stiff, harder to polish |
| Invar | 1200 | 148 | Metallic, easier machining |

**Recommendation**: Zerodur® Grade 0 (CTE < 5 ppb/K at 20°C) or ULE®.

### 4.2 Fabrication Steps

1. **Blank preparation**: Obtain glass-ceramic blank of appropriate size (>700 mm × 700 mm for collector).
2. **Rough grinding**: CNC grinding machine, diamond cup wheel, remove ~2 mm stock to achieve rough ellipsoidal shape, surface figure error ~10 µm.
3. **Fine grinding**: Smaller diamond wheels or bound abrasive, reduce to ~100 nm figure error.
4. **Polishing**: Computer-controlled optical surfacing (CCOS) with pitch lap or magnetorheological finishing (MRF). Target: surface figure ≤ 0.3 nm rms, roughness ≤ 0.15 nm rms.
5. **Metrology loop**:
   - Measure with stitching interferometry (Fizeau interferometer + CGH for asphere verification).
   - Compare to design prescription.
   - Apply differential correction polish.
   - Repeat until convergence.
6. **Ion Figuring**: Ion beam figuring (IBF) for final nanometer-level correction.
7. **Cleaning**: Ultrasonic + megasonic cleaning, UV/ozone cleaning, cleanroom handling only.

### 4.3 Surface Specification

| Specification | Value |
|---|---|
| Figure error (rms) | ≤ 0.1 nm (λ_EUV/135) |
| Mid-spatial frequency error | ≤ 0.1 nm rms (1–50 mm⁻¹) |
| Roughness (rms, spatial < 1 mm) | ≤ 0.15 nm |
| Clear aperture | ≥ 95% of 600 mm diameter |

---

## 5. Mirror Mount and Thermal Design

### 5.1 Thermal Load

The collector mirror absorbs:
- Reflected EUV (~33% of collected EUV, due to 67% reflectance).
- Out-of-band radiation (DUV, visible, IR from plasma): typically 10–50× larger than in-band EUV.
- CO₂ laser light not absorbed by plasma (~10% of laser power for misses).

**Estimated thermal power absorbed**: 0.5–5 kW (depending on shielding).

### 5.2 Cooling Design

1. **Cooling channels**: Laser-sintered or machined channels in the Zerodur back plate (or separate metal cooling manifold bonded to substrate).
2. **Coolant**: Ultra-pure water (UPW), 18 MΩ·cm resistivity, filtered < 0.1 µm.
3. **Flow rate**: ~5–20 L/min (sufficient to limit ΔT < 0.5 K across mirror).
4. **Temperature stability**: ±0.1 K (to keep thermal figure change below 0.05 nm rms).
5. **Thermal FEA**: Model heat distribution using ANSYS or FreeCAD/CalculiX; verify that figure change is acceptable.

### 5.3 Mirror Mount

- **Kinematic mount**: 3-point Kelvin clamp with flexure blades on the Invar support structure.
- **Degrees of freedom**: Fixed in all 6 DOF at nominal aligned position.
- **Adjustment**: 5-axis manual adjustment for initial alignment (tilt X/Y, tip, shift X/Y); one permanent axis (Z) for installation only.
- **Natural frequency**: First resonance ≥ 50 Hz (verify by FEA and modal test).

---

## 6. In-Situ Cleaning

Tin contamination on the collector reduces reflectance over time:

### 6.1 H₂ Plasma Etching

```
Chemical reaction: Sn + 2H· → SnH₂ (volatile, removed by vacuum)
                  Sn + 4H· → SnH₄ (stannane, volatile)

Process conditions:
    H₂ pressure: 10–50 Pa
    RF power: 100–500 W
    Duration: 10–60 min per cleaning cycle
    Temperature: < 200°C (prevent thermal damage to multilayer)
```

### 6.2 Cleaning Cycle Trigger

- Monitor in-situ EUV reflectance sensor (small Si photodiode behind collector).
- Trigger cleaning when reflectance drops > 1% from baseline.
- Typical interval: every 10⁹–10¹⁰ pulses (days of operation).

---

## 7. References

1. K. Ota et al., "EUV multilayer mirror design and fabrication," *Proc. SPIE* 8679, 2013.
2. S. Bajt et al., "Improved reflectance and stability of Mo/Si multilayers," *Opt. Eng.* 41, 2002.
3. E. Spiller, *Soft X-Ray Optics*, SPIE Press, 1994.
4. V. Bakshi (Ed.), *EUV Lithography*, 2nd ed., SPIE Press, 2018, Ch. 4.
5. C. Montcalm et al., "Survey of EUV multilayer mirror technology," *Proc. SPIE* 3331, 1998.
