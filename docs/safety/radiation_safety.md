# Radiation Safety — EUV and X-Ray

## ⚠️ Important Disclaimer

This document provides engineering guidance for understanding and controlling radiation hazards in an EUV lithography system. **It does not replace formal radiation safety training, institutional review, or regulatory compliance.** Always consult a qualified Radiation Safety Officer (RSO) and comply with all applicable local, national, and international regulations before constructing or operating any EUV or X-ray generating system.

---

## 1. Radiation Sources in an EUV System

### 1.1 EUV Photons (13.5 nm, 92 eV)

EUV photons at 92 eV are classified as **non-ionizing radiation** by some standards (ionization threshold ~12.4 eV for oxygen), but they are energetic enough to:
- Damage biological tissue (particularly eyes, skin) with high doses.
- Ionize gas molecules (producing ozone, NOx).
- Be fully absorbed by air within millimeters → **contained within vacuum enclosure**.

**Outside the vacuum**: EUV photons pose essentially no hazard because they are absorbed before exiting any vacuum window or enclosure opening. The vacuum enclosure is itself the primary barrier.

### 1.2 Soft X-Rays (Secondary)

The LPP plasma also emits bremsstrahlung and characteristic X-rays from hot Sn ions:
- Energy range: 1–100 keV.
- 1–10 keV (soft X-rays): absorbed by thin Al or stainless steel shielding.
- 10–100 keV (hard X-rays): require several mm of lead or steel shielding.

**X-rays are the primary radiation hazard that can escape the system**.

### 1.3 CO₂ Laser (10.6 µm, Class 4)

See [`laser_safety.md`](laser_safety.md) for CO₂ laser hazards.

---

## 2. Radiation Survey and Shielding Design

### 2.1 Regulatory Limits

| Organization | Occupational dose limit | Public dose limit |
|---|---|---|
| ICRP | 20 mSv/year (5-year average) | 1 mSv/year |
| US NRC (10 CFR 20) | 50 mSv/year | 1 mSv/year |
| EU (Council Directive 2013/59/Euratom) | 20 mSv/year | 1 mSv/year |
| Japan (RI Law) | 50 mSv/year | 1 mSv/year |

**Design target**: < 0.1 µSv/h at any accessible point outside the system enclosure (< 1 mSv/year for 2000 h/year occupation).

### 2.2 Shielding Calculation (Simplified)

For a point source of X-rays with energy E:
```
Dose rate at distance d from source:
    H_dot = A × Γ / d²
where:
    A = source activity (mCi equivalent) or power
    Γ = dose rate constant for energy E
    d = distance (cm)

With shielding of thickness x (material Z):
    H_dot_shielded = H_dot_unshielded × exp(-µ × x)
where:
    µ = mass attenuation coefficient (cm²/g) × density (g/cm³)

Example: 50 keV X-rays, lead shield:
    µ_Pb = 13.0 cm⁻¹ at 50 keV
    To reduce by factor 1000: x = ln(1000) / 13.0 = 0.53 cm of Pb
```

### 2.3 Shielding Materials

| Material | Effective X-ray energy | Thickness for 10× attenuation |
|---|---|---|
| Stainless steel (SS316) | 10–100 keV | 5–15 mm |
| Lead (Pb) | 10–100 keV | 1–5 mm |
| Tungsten | 10–100 keV | 0.5–3 mm |
| Concrete | 100 keV–10 MeV | 5–20 cm |

**Recommendation**: Design the source chamber walls from 10–20 mm thick 316L SS; supplement with 2 mm Pb sheet on high-flux directions. Total attenuation should be > 10,000× at the chamber exterior.

### 2.4 Radiation Survey

After initial assembly and before first operation:
1. Conduct a **radiation survey** with a calibrated Geiger-Müller (GM) tube or ion chamber.
2. Measure dose rate at: all enclosure exterior surfaces, service connection points, control room.
3. Document measurements and compare to design targets.
4. Add additional shielding where measured dose rates exceed targets.
5. Repeat survey annually or after any significant modification.

---

## 3. Interlocks and Access Control

### 3.1 Physical Interlocks

1. **Source enclosure doors**: Magnetic interlocks that physically cut the CO₂ laser beam and shut off the source if any door is opened.
2. **Keyed access**: Two-key interlock system — requires two independent keyholders to enable laser operation.
3. **Warning lights**: Amber (standby), red (laser/X-ray ON) at all enclosure entry points.
4. **Emergency stop (E-stop)**: Red E-stop buttons at each access point, in the control room, and at regular intervals in the cleanroom. E-stop cuts all laser power and vents the laser beam to a beam dump.

### 3.2 Administrative Controls

1. **Radiation Safety Officer (RSO)**: Designate a qualified RSO responsible for all radiation safety aspects.
2. **Training**: All personnel who enter the controlled area must receive documented radiation safety training.
3. **Dosimetry**: Issue personal dosimeters (film badge or TLD) to all regularly exposed personnel.
4. **Posted areas**: Post radiation areas with ANSI standard radiation warning signs.
5. **Logbook**: Record all source operating hours, radiation survey results, and personnel exposures.

---

## 4. Ozone and Toxic Gas Hazards

EUV photons absorbed by air produce ozone (O₃) and NOx:
- **Threshold**: O₃ at >0.1 ppm causes respiratory irritation.
- **Mitigation**: Ensure all EUV beam paths remain in vacuum; provide ventilation in equipment area.
- **Monitoring**: Ozone monitor (electrochemical or UV photometric) with alarm at 0.1 ppm.

Sn plasma reaction by-product: **SnH₄ (stannane)** — highly toxic (TWA: 0.1 ppm).
- **Handling**: Exhaust gas from source TMP passes through cryogenic trap before room discharge.
- **Monitoring**: Sn concentration monitor in equipment exhaust.

---

## 5. X-Ray Classification (USA)

In the United States, EUV lithography systems that generate X-rays are regulated under:
- **21 CFR 1020**: FDA regulations for radiation-producing electronic products.
- **Manufacturer registration**: Must register with FDA's Center for Devices and Radiological Health (CDRH) if manufactured for commercial sale.
- **State regulations**: Many states have additional X-ray facility registration requirements.

---

## 6. References

1. ICRP Publication 103, *The 2007 Recommendations of the International Commission on Radiological Protection*, 2007.
2. NCRP Report No. 151, *Structural Shielding Design and Evaluation for Megavoltage X- and Gamma-Ray Radiotherapy Facilities*, 2005.
3. ANSI Z535.2, *American National Standard for Environmental and Facility Safety Signs*.
4. NIST, *X-Ray Mass Attenuation Coefficients*, [physics.nist.gov/xaamdi](https://physics.nist.gov/PhysRefData/XrayMassCoef/).
5. B. Henke et al., "X-Ray Interactions: Photoabsorption, Scattering," *At. Data Nucl. Data Tables* 54, 1993.
