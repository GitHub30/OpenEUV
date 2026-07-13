# Vacuum System — Detailed Design

## 1. Overview

EUV radiation at 13.5 nm is absorbed by any gas (1/e absorption length in air at STP ≈ 50 nm; even at 1 Pa, the absorption length is only ~5 cm). Therefore the entire EUV beam path must be evacuated to < 1 × 10⁻³ Pa.

---

## 2. Vacuum Zones and Pressure Requirements

| Zone | Target Pressure | Primary Pump | Notes |
|---|---|---|---|
| Source chamber | 1 × 10⁻⁴ Pa base; ~10 Pa operating (H₂) | TMP 2000 L/s | H₂ buffer gas for debris mitigation |
| Collector chamber | 1 × 10⁻³ Pa | TMP 1000 L/s | Differential pumping from source |
| ILS chamber | 5 × 10⁻⁴ Pa | TMP 500 L/s | Illumination optics |
| POB chamber | 1 × 10⁻⁵ Pa | TMP 500 L/s + ion pump | Ultra-clean for mirror lifetime |
| Wafer station | 1 × 10⁻³ Pa | TMP 300 L/s | During exposure |
| Reticle station | 1 × 10⁻³ Pa | TMP 300 L/s | During exposure |
| Loadlock (wafer) | 1 Pa (pump-down) | Dry scroll pump | 30 s pump-down cycle |
| Loadlock (reticle) | 1 Pa (pump-down) | Dry scroll pump | 30 s pump-down cycle |

---

## 3. Pumping System Design

### 3.1 Turbomolecular Pumps (TMP)

- **Type**: Magnetically levitated (maglev) TMP — no vibration, no oil.
- **Manufacturers**: Pfeiffer, Edwards, Leybold.
- **Selection criteria**: Pumping speed × compression ratio ≥ required gas throughput.

**Example sizing (POB chamber)**:
```
Gas load from outgassing:
    Q_out = q_ss × A_surface (q_ss ≈ 10⁻⁷ Pa·m³/s·m² for baked SS)
    A_surface ≈ 5 m²
    Q_out = 10⁻⁷ × 5 = 5 × 10⁻⁷ Pa·m³/s

Required pumping speed:
    S = Q / P_target = 5 × 10⁻⁷ / 10⁻⁵ = 0.05 m³/s = 50 L/s

Margin factor 10 → S = 500 L/s TMP
```

### 3.2 Backing Pumps (Roughing)

- **Type**: Dry scroll pump or multi-stage roots pump (oil-free, no contamination).
- **Function**: Back the TMP (maintain < 1 Pa at TMP exhaust), pump loadlocks.
- **Typical size**: 12–30 m³/h per TMP.

### 3.3 Ion Pumps

- **Location**: POB chamber (supplemental, for ultra-clean base pressure).
- **Function**: Getter-pump noble gases and active gases without vibration or oil.
- **Typical size**: 100–500 L/s.
- **Note**: Ion pumps cannot be used as primary pumps; require backing TMP to reach starting pressure.

### 3.4 Cryogenic Panels

- **Location**: POB and ILS chambers.
- **Function**: Cryocondensation of residual hydrocarbons (water, CO₂, VOC).
- **Temperature**: 80 K (LN₂-cooled) or 15 K (closed-cycle cryo) for CO/N₂ capture.
- **Benefit**: Reduces hydrocarbon partial pressure to < 10⁻⁸ Pa, preventing mirror carbon growth.

---

## 4. Vacuum Chamber Construction

### 4.1 Materials

- **Body**: 316L stainless steel (electropolished, Ra ≤ 0.4 µm internal surfaces).
- **Flanges**: CF (ConFlat®) flanges with oxygen-free copper (OFC) or aluminum gaskets.
- **Windows**: ZnSe (for CO₂ laser), MgF₂ (for UV diagnostics), viewports: borosilicate with CF flange.
- **Seals**: No elastomers (silicone, Viton) in high-vacuum zones — elastomers outgas organics that contaminate mirrors.

### 4.2 Design Rules

1. **Surface area minimization**: Every internal surface outgasses; minimize unnecessary internal structure.
2. **Trapped volumes**: All internal cavities must be vented to the vacuum with drilled holes to prevent virtual leaks.
3. **Roughness**: Electropolish all stainless surfaces to Ra ≤ 0.4 µm (reduces outgassing by ~10×).
4. **Welds**: Full-penetration welds, no crevices; helium leak-test all welds to < 10⁻¹⁰ Pa·m³/s.
5. **Materials to avoid**: Zinc, cadmium, mercury, sulfur compounds, phosphorus-containing lubricants (all contaminate Mo/Si coatings).

### 4.3 Feedthroughs

| Type | Standard | Notes |
|---|---|---|
| Electrical | CF-mounted ceramic-to-metal sealed | Multiple pins available |
| RF coaxial | SMA or N-type with CF flange | For diagnostics |
| Motion | Rotary feedthrough (ferrofluidic or bellows) | For valve actuators |
| Cooling | Welded tubes with compression fitting | For water cooling lines |
| Gas | VCR or CF gas inlet with leak valve | For H₂, purge gas |

---

## 5. Bake-Out Procedure

Baking removes adsorbed water and light organics from chamber surfaces, reducing long-term outgassing rate by 10–100×.

### 5.1 Bake-Out Protocol

1. **Install all components** (mirrors, stages, sensors) — bake with components in situ where possible.
2. **Heat to 150°C**: Resistive heater tape + aluminum foil insulation, temperature ramp ≤ 10°C/min.
3. **Duration**: 48–72 hours at 150°C while pumping with TMP.
4. **Monitor**: Residual gas analyzer (RGA) — bake is complete when H₂O peak falls below 10⁻⁷ Pa partial pressure.
5. **Cooldown**: ≤ 2°C/min to prevent thermal shock to glass/ceramic components.
6. **Target base pressure**: < 5 × 10⁻⁶ Pa (without H₂ injection) after bake-out.

**Temperature limits** for heat-sensitive components:
- Mo/Si multilayer mirrors: max 200°C (above this, Mo₅Si₃ formation degrades reflectance).
- Piezo actuators: max 120°C.
- Electronics: bake separately or shield from heat.

---

## 6. Differential Pumping Between Zones

The source chamber operates at high pressure (10 Pa H₂) while the optical chambers must be < 10⁻³ Pa. A differential pumping section with aperture and dedicated TMP separates them.

### 6.1 Aperture Design

```
EUV passes through aperture (diameter D) between source and ILS.
Gas conductance through aperture: C = 11.6 D² L/s (for air, D in cm)
Example: D = 5 mm = 0.5 cm → C = 11.6 × 0.25 = 2.9 L/s

Gas flow from source to ILS: Q = C × (P_source - P_ILS) ≈ 2.9 × 10 = 29 Pa·L/s

Pumping required at ILS to maintain P_ILS = 10⁻³ Pa:
    S_ILS = Q / P_ILS = 29 / 10⁻³ = 29,000 L/s  →  too large!

Solution: Add intermediate differential pump stage between source and ILS.
    Add second aperture (D=3mm) with 2000 L/s TMP in between.
    Intermediate pressure: P_int = Q_from_source / S_int
        = 2.9 × 10 / 2000 = 0.015 Pa
    Gas reaching ILS: Q = C_2 × P_int = (11.6 × 0.09) × 0.015 = 0.016 Pa·L/s
    Required S_ILS = 0.016 / 5×10⁻⁴ = 32 L/s  → achievable with small TMP
```

### 6.2 EUV Transmission Through Aperture

The aperture must pass ≥ 95% of the EUV beam étendue. Design the aperture to be slightly larger than the beam cross-section at that point, accounting for divergence from the intermediate focus.

---

## 7. Hydrogen Gas Handling

H₂ is used in the source chamber for debris mitigation. Safety precautions are critical.

### 7.1 H₂ System Design

- **Supply**: Ultra-high purity H₂ (99.9999%), from compressed gas cylinder with regulator.
- **Flow control**: Mass flow controller (MFC), range 0–200 sccm, ±0.5% accuracy.
- **Pressure monitoring**: Capacitance manometer (1 Pa full scale) in source chamber.
- **By-product handling**: SnH₄ (stannane, highly toxic) — cryogenically trapped before TMP exhaust; never exhaust directly to room.
- **Exhaust**: H₂ exhaust through TMP, then through a palladium catalytic converter (converts H₂ → H₂O before venting).

### 7.2 Safety Interlocks

- H₂ concentration monitor in equipment enclosure: alarm at 1% (LEL = 4%), shutdown at 2%.
- Solenoid shut-off valve on H₂ supply line, normally-closed.
- Automatic purge with N₂ on system shutdown.

See [`docs/safety/laser_safety.md`](../safety/laser_safety.md) for additional H₂ safety details.

---

## 8. Vacuum System Monitoring

| Sensor | Type | Range | Location |
|---|---|---|---|
| Ion gauge | Bayard-Alpert | 10⁻¹⁰ – 10⁻¹ Pa | All high-vacuum chambers |
| Capacitance manometer | MKS Baratron | 0–100 Pa | Source chamber, loadlocks |
| RGA | Quadrupole mass spec | 1–200 amu | POB, ILS (one each) |
| Thermocouple gauge | Pirani | 10⁻¹ – 10⁵ Pa | Roughing lines |

---

## 9. References

1. J. O'Hanlon, *A User's Guide to Vacuum Technology*, 3rd ed., Wiley, 2003.
2. N. Harris, *Modern Vacuum Practice*, 3rd ed., McGraw-Hill, 2005.
3. P. Kruit et al., "Vacuum system design for an EUV source," *J. Vac. Sci. Technol. B*, 2010.
4. Pfeiffer Vacuum, *The Vacuum Technology Book*, Vol. II, 2013.
5. CERN, Molflow+ simulation software, [https://molflow.web.cern.ch/](https://molflow.web.cern.ch/).
