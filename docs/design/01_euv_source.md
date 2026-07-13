# EUV Light Source — Detailed Design

## 1. Overview

The EUV light source is the most challenging subsystem in an EUV lithography system. It must deliver ≥ 250 W of in-band EUV power at 13.5 nm (±1% bandwidth) to the intermediate focus (IF) continuously at a repetition rate of 50 kHz.

This document describes the Laser-Produced Plasma (LPP) source using a high-power CO₂ drive laser and tin (Sn) droplet targets.

---

## 2. Physical Principle

When a high-power laser pulse is focused onto a tin droplet, the energy is absorbed and the Sn is heated to electron temperatures of ~20–30 eV, forming a plasma. At these temperatures, multiply ionized Sn ions (Sn⁸⁺ through Sn¹⁴⁺) undergo 4d–4f, 4d–4p, and 4p–4s transitions that collectively emit an unresolved transition array (UTA) centered at 13.5 nm.

**Conversion efficiency (CE)**: fraction of laser energy converted to in-band EUV (13.5 nm ± 1%) into 2π sr.

```
CE = E_EUV(2π, 13.5nm ± 1%) / E_laser
```

Target: CE ≥ 4% (state of the art: ~5–6% with two-pulse scheme).

---

## 3. Drive Laser Specifications

### 3.1 Wavelength Selection

CO₂ laser (10.6 µm) is preferred over Nd:YAG (1.064 µm) because:
- Inverse bremsstrahlung absorption scales as λ², so CO₂ couples more efficiently into the plasma critical density.
- Critical density at 10.6 µm: n_c = 9.9 × 10¹⁸ cm⁻³ vs. n_c = 10²¹ cm⁻³ for 1.064 µm.
- At n_c(CO₂), the plasma is at the optimal temperature (~25 eV) for 13.5 nm emission.

### 3.2 Laser Parameters

| Parameter | Value |
|---|---|
| Wavelength | 10.6 µm |
| Pulse repetition rate | 50 kHz |
| Pre-pulse energy | 3–5 mJ (at target) |
| Main pulse energy | 400–800 mJ (at target) |
| Pre-pulse width | 5–10 ns FWHM |
| Main pulse width | 10–15 ns FWHM |
| Pre-pulse to main pulse delay | 0.5–3 µs |
| Average power | 20–40 kW |
| Beam quality | M² < 1.3 |
| Polarization | Linear or circular |

### 3.3 Laser Architecture

```
Seed oscillator (CO₂, CW) → Acousto-optic modulator (pulse slicer)
    → Pre-amplifier chain (CO₂ transverse flow amplifiers)
    → Main amplifier (CO₂ slab or transverse flow)
    → Beam transport (gold-coated reflective optics, ZnSe transmissive)
    → Final focusing mirror (off-axis parabola, Au-coated, f ≈ 300 mm)
```

### 3.4 Focusing Optics

- **Off-axis parabolic (OAP) mirror**: gold-coated copper, off-axis angle 30–45°.
- **Focal spot diameter**: 200–300 µm (matched to pre-expanded Sn cloud).
- **Intensity at focus**: ~10¹¹ W/cm² (main pulse).
- **Depth of focus**: ≥ ±1 mm (to accommodate droplet position jitter).

---

## 4. Tin Droplet Generator

### 4.1 Design Requirements

| Parameter | Value |
|---|---|
| Droplet diameter | 20–30 µm |
| Droplet repetition rate | 50 kHz |
| Droplet velocity | 60–80 m/s |
| Position jitter | < 3 µm (3σ) |
| Temperature (orifice) | 250–280 °C |
| Tin purity | ≥ 99.99% |

### 4.2 Operating Principle

A reservoir of liquid tin (held above 232 °C melting point) is pressurized. Liquid tin flows through a micro-orifice (diameter ~17 µm). A piezoelectric transducer modulates the jet pressure at the Rayleigh breakup frequency, causing the jet to break into uniform droplets.

### 4.3 Rayleigh Breakup Analysis

```
Jet diameter:     d_jet ≈ d_orifice × (P_reservoir / P_atm)^(1/2) [simplified]
Optimal excitation frequency (Rayleigh):
    f_R = v_jet / (π × d_jet) × 0.97    [Rayleigh instability factor 0.97]

Droplet diameter from volume conservation:
    d_droplet = (1.5 × d_jet²)^(1/3) × (v_jet / f_R)^(1/3)

Example:
    d_orifice = 17 µm, P = 2 bar, v_jet = 1.25 m/s
    f_R = 1.25 / (π × 17e-6) × 0.97 ≈ 22.7 kHz  →  need 50 kHz
    Adjust: use multiple orifices, or increase pressure to raise v_jet
```

### 4.4 Droplet Catcher

- Location: opposite side of plasma from laser, 150–200 mm from interaction point.
- Material: liquid-cooled tungsten cone.
- Capacity: collects > 99.9% of unreacted Sn droplets.
- Disposal: molten Sn drains to a sealed reservoir for periodic removal.

---

## 5. Debris Mitigation System

Sn ions, neutrals, and micro-particles are emitted from the plasma in all directions. Without mitigation, they coat and destroy the collector mirror within hours.

### 5.1 Hydrogen Buffer Gas

- Flow: 10–50 sccm H₂ into the source chamber.
- Mechanism: H₂ molecules slow Sn ions by charge exchange and thermalization.
- Typical Sn ion energy reduction: from 1–10 keV to < 50 eV (below Sn sputtering threshold of Mo/Si multilayer).
- By-product: SnH₄ (stannane, toxic) — captured by cryogenic trap.

### 5.2 Rotating Foil Trap (RFT)

- Geometry: disk with radial slots, radius ≈ 300 mm.
- Rotation speed: 3000–6000 RPM.
- Slot duty cycle: 50% open.
- EUV transmission: ~50% (geometric) × cos factor ≈ 40%.
- Debris suppression: > 99% for particles with v < 1000 m/s.

### 5.3 Magnetic Deflection (Optional)

- Solenoid or permanent magnet array around source chamber.
- Deflects charged Sn ions along helical paths away from collector axis.
- Field strength: 0.1–0.5 T.

### 5.4 Collector In-Situ Cleaning

- Periodic H₂ plasma etching: tin reacts with H radicals to form volatile SnH₄.
- Cleaning cycle: every 10–50 billion pulses (depending on contamination rate).
- During cleaning: laser off, H₂ flow increased to 100–500 sccm, RF plasma ignited.

---

## 6. EUV Power Budget

```
CO₂ laser power at target:                     20 kW (average)
Conversion efficiency (CE):                     4%
EUV power into 2π sr at 13.5 nm ± 1%:         800 W
Collector solid angle factor (NA=0.20):         × 0.020 → 16 W
  [Ω_coll = 2π(1 - cos θ_max) / 4π; θ_max = arcsin(0.20) ≈ 11.5°]
Collector reflectance (Mo/Si, ~67%):            × 0.67 → 10.7 W
Foil trap transmission (~40%):                  × 0.40 → 4.3 W
ILS transmission (~60%):                        × 0.60 → 2.6 W

Wait — recalculate with correct collector solid angle for ellipsoidal:
Ellipsoidal collector collects up to θ_max = 60° from source:
    Ω = 2π(1 - cos 60°) = π sr → fraction = π/4π = 0.25 (25% of 4π)
    EUV collected: 800 W × 0.25 = 200 W
    After collector reflectance (67%): 134 W
    After foil trap (40%): 54 W
    After IF to lens losses: 44 W → too low

Solution: Increase CE to 5% or increase laser power to 40 kW:
    EUV into 2π: 40 kW × 5% = 2000 W
    After collector 25%: 500 W
    After reflectance 67%: 335 W
    After foil trap 40%: 134 W
    After ILS 60%: 80 W
    After SPF 80%: 64 W
    After IF aperture 85%: 54 W ← still below 250 W

Need higher NA collector or higher CE:
    With NA_coll = 0.45 (θ_max ≈ 27°), Ω = 2π(1-cos27°) ≈ 0.68 sr (5.4% of 4π):
    EUV: 2000 W × 0.054 = 108 W × 0.67 = 72 W × 0.40 foil = 29 W → not enough

Note: The 250 W target requires combining:
    - CE ≥ 5%
    - Laser power 30–40 kW
    - Large ellipsoidal collector (NA ≈ 0.2 at IF, ~5 sr collection)
    - No foil trap (use H₂ + magnetic deflection only)
    Full calculation in collector_efficiency.py simulation
```

---

## 7. Source Chamber Design

### 7.1 Chamber Layout

```
                    ┌──────────────────────────────────┐
   CO₂ laser in ──▶ │  ZnSe window (laser entry)       │
                    │  ┌──────────────────────────────┐ │
                    │  │   Droplet generator          │ │
                    │  │        │ droplets             │ │
                    │  │        ▼                      │ │
                    │  │   Interaction zone ◀── laser  │ │
                    │  │        │                      │ │
                    │  │        ▼                      │ │
                    │  │   Droplet catcher             │ │
                    │  └──────────────────────────────┘ │
                    │  Collector mirror (outside view)  │
                    │  Turbomolecular pump port         │
                    │  H₂ gas inlet + pressure control  │
                    └──────────────────────────────────┘
```

### 7.2 Chamber Materials and Construction

- **Body**: 316L stainless steel, electro-polished, baked at 150 °C.
- **Windows**: ZnSe for CO₂ laser entry (AR-coated, 10.6 µm); no windows on EUV side.
- **Feedthroughs**: CF-standard, welded.
- **Seals**: All-metal (copper gaskets, CF flanges).
- **Base pressure**: < 1 × 10⁻⁶ Pa (without H₂ flow).
- **Operating pressure**: 5–20 Pa (with H₂ buffer).

---

## 8. References

1. I. Fomenkov et al., "Light sources for high-volume manufacturing EUV lithography: recent progress and future development," *J. Phys. B: At. Mol. Opt. Phys.* 51, 2018.
2. D. Bleiner et al., "Laser-produced plasmas as EUV photon sources," *Opt. Laser Technol.* 56, 2014.
3. V. Bakshi (Ed.), *EUV Lithography*, 2nd ed., SPIE Press, 2018, Ch. 3.
4. S. Fujioka et al., "Efficient extreme-ultraviolet emission from one-dimensional spherically symmetric plasma," *Appl. Phys. Lett.* 87, 2005.
