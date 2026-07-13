# Illumination System — Detailed Design

## 1. Overview

The illumination system (ILS) receives EUV from the collector intermediate focus (IF) and transforms it into a uniform, shaped illumination field at the reticle plane. It must provide programmable illumination modes (conventional, annular, dipole, quadrupole) while maintaining < ±0.3% dose uniformity across the scanning slit.

---

## 2. Optical Layout

```
IF (point source) → Spectral Purity Filter (SPF)
                  → Collimating mirror
                  → Field Facet Mirror (FFM)
                  → Pupil Facet Mirror (PFM)
                  → Transfer optics (2–4 grazing incidence mirrors)
                  → Reticle plane
```

All mirrors are reflective (no transmissive elements in the EUV path).

---

## 3. Spectral Purity Filter (SPF)

### 3.1 Purpose

The plasma source emits not only 13.5 nm EUV but also out-of-band radiation:
- DUV (100–300 nm): partially transmitted by optical coatings, exposes resist.
- IR (10.6 µm CO₂): heats optical elements, can degrade resist.
- Visible: minor contributor.

The SPF must suppress DUV by > 10⁶ and IR by > 10⁶, while transmitting ≥ 80% of 13.5 nm EUV.

### 3.2 SPF Options

| Type | EUV transmission | DUV suppression | Notes |
|---|---|---|---|
| Transmissive grating (Zr foil) | ~60–80% | ~10⁵ | Degrades with EUV dose |
| Grazing incidence mirror (SiO₂) | ~90% | ~10⁴–10⁶ | Depends on angle + coating |
| Multi-layer filter (Zr/Mo) | ~50–70% | ~10⁶ | Fragile |

**Recommended**: Grazing incidence Si or SiO₂ mirror at θ_grazing ≈ 5–10°; low reflectance for IR, high reflectance for EUV.

---

## 4. Field Facet Mirror (FFM)

### 4.1 Function

The FFM is an array of small rectangular mirrors, each tilted slightly differently. Each facet creates a virtual source image at the pupil plane (PFM). The array of virtual sources at the pupil provides spatial incoherence, homogenizing the illumination field.

### 4.2 FFM Design

```
Required slit at reticle: 26 mm × 5 mm
ILS magnification: M_ILS
Facet size at FFM: f_w × f_h = (26/M_ILS) × (5/M_ILS)

Typical M_ILS ≈ 3.5:
    Facet at FFM: 7.4 mm × 1.4 mm

Number of facets: N_facet = π r²_FFM / (f_w × f_h)
    For r_FFM = 100 mm: N ≈ π × 10000 / 10.36 ≈ 3030 facets (over-packed, hexagonal ~200)
```

Practical number of facets: 100–200 (rectangular array, not all locations used).

### 4.3 Facet Radius of Curvature

Each facet is slightly curved to image the source point into a small spot at the reticle plane (in the non-scanning direction) or at the pupil:

```
Thin lens formula: 1/f = 1/u + 1/v
where u = distance from IF to FFM, v = distance from FFM to reticle
For u = 800 mm, v = 1200 mm:
    f = (800 × 1200) / (800 + 1200) = 480 mm
    R = 2f (concave mirror) = 960 mm
```

### 4.4 Facet Tilts

Each facet is tilted by a small angle to redirect its portion of the beam to the correct slit location at the reticle. The tilt pattern is optimized by ray-tracing to minimize non-uniformity.

---

## 5. Pupil Facet Mirror (PFM)

### 5.1 Function

The PFM is located at the pupil plane of the ILS. Each PFM facet corresponds to one FFM facet; the PFM facet reflects the beam from the FFM facet to the same slit location at the reticle, but from a different angle (pupil position). This fills the pupil with multiple source images, enabling controllable illumination modes.

### 5.2 Illumination Modes

| Mode | PFM facets enabled | Sigma inner | Sigma outer |
|---|---|---|---|
| Conventional | All | 0 | 0.80 |
| Annular | Outer ring | 0.60 | 0.80 |
| Dipole (Y) | Top and bottom clusters | — | — |
| Dipole (X) | Left and right clusters | — | — |
| Quadrupole | Four clusters at ±45° | — | — |

For programmable illumination, individual facets or rows can be switched "off" by tilting them out of the optical path (actuated facets with piezo actuators or MEMS mirrors).

---

## 6. Transfer Optics

### 6.1 Purpose

After the PFM, grazing incidence mirrors relay the beam to the reticle masking blades and the reticle plane. They also set the telecentricity (ensure chief ray arrives perpendicular to reticle).

### 6.2 Typical Layout

- 2–4 grazing incidence Ni or Ru-coated toroidal mirrors.
- Grazing angle: 10–15° (for high EUV reflectance of Ni/Ru at 13.5 nm).
- Function: anamorphic correction, beam shaping, telecentricity setting.

---

## 7. Uniformity Analysis

### 7.1 Uniformity Measurement

Slit uniformity is measured with an EUV-sensitive photodiode or CCD behind a reflective mask at the reticle plane. Raster scan or full-field measurement.

### 7.2 Uniformity Budget

| Contribution | Budget (3σ) |
|---|---|
| FFM tilt errors | ±0.15% |
| Multilayer reflectance variation across facets | ±0.10% |
| PFM facet tilt errors | ±0.10% |
| Transfer optics reflectance variation | ±0.05% |
| **Total RSS** | **±0.21%** |

Target: < ±0.3% (3σ) total.

### 7.3 Active Correction

Small actuators on individual FFM facets (piezo tilt platforms) can dynamically adjust tilt angles to compensate measured non-uniformity. Correction resolution: 0.1 µrad per facet.

---

## 8. Throughput Budget

| Element | EUV transmission/reflectance |
|---|---|
| SPF (grazing Si) | 85% |
| FFM (Mo/Si × 1) | 67% |
| PFM (Mo/Si × 1) | 67% |
| Transfer mirrors × 2 (Ru, grazing) | 60% each → 36% |
| **Total ILS transmission** | **0.85 × 0.67 × 0.67 × 0.36 ≈ 13.7%** |

---

## 9. References

1. N. Harned et al., "EUV development at ASML: the alpha demo tool program," *Proc. SPIE* 6517, 2007.
2. M. Antoni et al., "Illumination optics design for EUV lithography," *Proc. SPIE* 3997, 2000.
3. P. Naulleau et al., "Characterization of the optical performance of EUV illumination system," *Proc. SPIE* 5037, 2003.
4. V. Bakshi (Ed.), *EUV Lithography*, 2nd ed., SPIE Press, 2018, Ch. 6.
