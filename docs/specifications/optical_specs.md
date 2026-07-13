# Optical Specifications and Prescriptions

## 1. Collector Mirror

### 1.1 Optical Prescription

| Parameter | Value |
|---|---|
| Shape | Prolate ellipsoid of revolution |
| Semi-major axis a | 850 mm |
| Semi-minor axis b | 400 mm |
| Source focal distance (c₁) | ~750 mm |
| Image focal distance (c₂) | ~950 mm |
| Vertex-to-source distance | 100 mm |
| Collection half-angle | 0°–60° |
| Central obscuration half-angle | ~6° (80 mm dia. at 100 mm) |

### 1.2 Multilayer Specification

| Layer | Material | Thickness |
|---|---|---|
| Bilayer period d(θ) | Graded 6.9–19.7 nm | Varies with incidence angle |
| Mo fraction | 0.40 | Optimized for peak reflectance |
| Number of bilayers | 50 | |
| Cap layer | Si | 4 nm |
| Peak reflectance (near-normal) | ≥ 67% | At 13.5 nm |

---

## 2. Illumination System

### 2.1 Field Facet Mirror (FFM)

| Parameter | Value |
|---|---|
| Substrate shape | Flat or mildly curved (R ≈ 960 mm) |
| Facet dimensions | 7.4 mm × 1.4 mm (nominal) |
| Number of facets | 122 (active), 200 (total including spares) |
| Facet array diameter | ~120 mm |
| Coating | Mo/Si, ~67% reflectance |
| Tilt range per facet | ±15 mrad |
| Tilt resolution | 0.1 µrad (with piezo actuation) |

### 2.2 Pupil Facet Mirror (PFM)

| Parameter | Value |
|---|---|
| Number of facets | Equal to FFM active facets (122) |
| Pupil diameter | ~100 mm |
| Facet shape | Circular, ~6 mm diameter |
| Coating | Mo/Si, ~67% reflectance |
| Max pupil fill | σ_outer = 0.9 |

---

## 3. Projection Optics Box (6-Mirror System)

### 3.1 System Summary

| Parameter | Value |
|---|---|
| Wavelength | 13.5 nm |
| Magnification | -0.25 (4× reduction) |
| Image NA | 0.33 |
| Image field radius (chief ray) | 30 mm from axis |
| Image field size | 26 mm × 2 mm |
| Reticle-to-wafer distance | ~1400 mm |

### 3.2 Mirror Prescriptions (Nominal Design)

Note: These are approximate prescriptions for a 0.33 NA, 4× EUV system. Exact values require full optical design optimization with a suitable tool (Zemax, Code V).

| Mirror | Type | Vertex R (mm) | Conic K | CA (mm) | Coating |
|---|---|---|---|---|---|
| M1 | Concave | -1200 | -0.87 | 800 | Mo/Si |
| M2 | Convex | +300 | -2.50 | 200 | Mo/Si |
| M3 | Concave | -600 | -0.60 | 400 | Mo/Si |
| M4 | Convex | +200 | -5.00 | 150 | Mo/Si |
| M5 | Concave | -900 | -0.75 | 700 | Mo/Si |
| M6 | Concave | -450 | -0.40 | 600 | Mo/Si |

Each mirror also has higher-order aspheric terms (A₄ through A₁₂) determined by the full optimization.

### 3.3 Mirror Coating Specification

| Parameter | Value |
|---|---|
| Multilayer type | Mo/Si, graded |
| Number of bilayers | 40–50 |
| Peak reflectance | ≥ 67% at design angle |
| Angular bandwidth (FWHM) | ~10° |
| Mid-spatial frequency roughness | < 0.1 nm rms (1–50 mm⁻¹) |
| High-spatial frequency roughness | < 0.05 nm rms (> 50 mm⁻¹) |

### 3.4 Wavefront Error Budget

| Source | Zernike group | Budget (nm rms) |
|---|---|---|
| Mirror figure errors (combined) | Z4–Z9 | 0.40 |
| Mirror alignment errors | Z4–Z9 | 0.30 |
| Coating phase errors | Z4, Z9 | 0.15 |
| High-order (Z10+) | all | 0.25 |
| Thermal drift (during exposure) | Z4–Z9 | 0.10 |
| **Total RSS** | | **≤ 0.59 nm rms** |

Design target: ≤ 0.96 nm rms total (including manufacturing and test uncertainty).

---

## 4. Imaging Performance

### 4.1 Resolution Limit

```
Rayleigh resolution: R = k₁ × λ / NA
    Rayleigh limit (k₁ = 0.61): R = 0.61 × 13.5 / 0.33 = 24.9 nm
    With PSM (k₁ = 0.32): R ≈ 13 nm half-pitch
    
Depth of focus (DOF):
    DOF = ± k₂ × λ / NA²
    Rayleigh DOF (k₂ = 0.5): DOF = ± 62 nm
```

### 4.2 Optical Transfer Function

```
Coherent cutoff frequency: f_c = NA / λ = 0.33 / 13.5 nm = 24.4 cycles/µm
Incoherent cutoff frequency: 2 × f_c = 48.9 cycles/µm
Corresponding minimum half-pitch:
    Coherent: 1/(2 f_c) = 20.5 nm
    Incoherent: 1/(4 f_c) = 10.2 nm (with optimized illumination)
```

---

## 5. Alignment and Overlay Optical Specifications

### 5.1 Alignment System

| Parameter | Value |
|---|---|
| Alignment wavelength | 633 nm (off-axis) |
| Alignment mark type | Diffraction grating (40 µm period) |
| Capture range | ±50 µm |
| Precision (3σ) | < 1 nm |
| Throughput per mark | < 1 s |

### 5.2 Overlay Targets

| Mark type | Size | Layer sensitivity |
|---|---|---|
| Box-in-box | 25 µm outer / 15 µm inner | 0.5 nm/pixel |
| AIM grating | 16 µm period | 0.2 nm per measurement |
