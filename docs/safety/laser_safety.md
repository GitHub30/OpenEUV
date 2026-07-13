# Laser Safety — High-Power CO₂ Laser

## ⚠️ Important Disclaimer

This document provides engineering guidance for understanding and controlling laser hazards in an EUV lithography system. **It does not replace formal laser safety training or institutional review.** All personnel working with Class 4 laser systems must complete documented laser safety training before working with or near the laser. Always comply with ANSI Z136.1, IEC 60825, and all applicable institutional and local regulations.

---

## 1. Laser Classification

The drive laser for an EUV LPP source is a **Class 4** laser:

| Parameter | Value |
|---|---|
| Wavelength | 10.6 µm (CO₂) |
| Average power | 20,000–40,000 W (20–40 kW) |
| Pulse energy | 0.4–0.8 J |
| Pulse duration | 10–15 ns |
| Repetition rate | 50,000 Hz (50 kHz) |
| Beam diameter (at output) | ~50 mm |
| Classification | Class 4 (far exceeds any AEL) |

**At 20 kW average power, even 0.1% stray reflection (~20 W) is a catastrophic hazard.** This laser is more powerful than most industrial cutting lasers and requires the most rigorous safety measures.

---

## 2. Hazards

### 2.1 Eye Hazard

CO₂ laser radiation at 10.6 µm is strongly absorbed by the cornea (water absorption):
- **Corneal burn**: Irreversible corneal damage possible from brief exposure to low power densities.
- **MPE (Maximum Permissible Exposure)**:
  ```
  For CW CO₂ (10.6 µm), exposure time t = 10 s:
  MPE = 100 mW/cm² (cornea)
  ```
- At 20 kW, even a reflection from an unintended surface at 10 m distance can easily exceed MPE.

### 2.2 Skin Hazard

- CO₂ laser radiation is absorbed in the top ~100 µm of skin (water absorption).
- At high power density: instant severe thermal burn.
- MPE (skin): 1 W/cm² (CW, t ≥ 10 s).

### 2.3 Fire Hazard

- 20 kW laser can instantly ignite most combustible materials.
- Reflected or scattered beams can ignite cleanroom garments, paper, cardboard.
- Beam dumps must be designed to absorb the full beam power without thermal runaway.

### 2.4 Fume Hazard

- High-power CO₂ laser ablation of tin produces tin oxide fumes (SnO, SnO₂) — toxic if inhaled.
- All ablation occurs inside the source chamber (vacuum) — no external fume hazard during normal operation.
- During maintenance: vent chamber with N₂, use appropriate respiratory protection.

---

## 3. Laser Protective Equipment (LPE)

### 3.1 Laser Eyewear

**NEVER look into or near the beam without appropriate certified eyewear**.

| Wavelength | Required OD | Standard |
|---|---|---|
| 10.6 µm (CO₂) | OD ≥ 6 (Class 4, > 10 kW) | ANSI Z136.1, EN 207 |

- **Lens material**: ZnSe or germanium opaque filters (do NOT use regular polycarbonate — not rated for CO₂).
- **Certification**: Must be marked with wavelength and OD rating per EN 207.
- **Inspection**: Inspect eyewear for scratches or damage before each use. Discard if damaged.

### 3.2 Beam Path Protection

- All beam paths must be enclosed (pipes, housings, or metal beam tubes) before the laser enters the source chamber.
- Beam tube material: stainless steel or aluminum, with beam dumps at all terminations.
- No unintended reflective surfaces (watches, jewelry, shiny tools) within the beam path enclosure.

---

## 4. Engineering Controls

### 4.1 Beam Enclosure

```
Laser head → Sealed beam transport pipe (SS, grounded)
                → ZnSe focusing window (AR-coated, 10.6 µm)
                → Source chamber (vacuum)
                    → Beam dump (water-cooled W/Cu, if beam misses target)
```

- The beam transport pipe must be interlocked: opening any section shuts down the laser.
- All penetrations (instrumentation, cooling) use beam-tight feedthroughs.

### 4.2 Beam Dumps

Every terminated beam path needs a beam dump:
- **Main beam dump**: Water-cooled tungsten/copper block inside source chamber.
- **Alignment beam dump**: Low-power alignment beam dump at IF alignment position.
- **Beam dump design**: Must absorb 120% of maximum beam power without temperature runaway.

```
Beam dump thermal calculation:
    P_max = 40 kW (full beam if misfire)
    Coolant flow: Q = P / (ρ × Cp × ΔT) = 40,000 / (1000 × 4186 × 10) = 0.96 L/s
    Design flow: 2 L/s for margin
    Material: Oxygen-free copper with tungsten insert at beam spot
```

### 4.3 Interlocks

**Hardware interlocks (relay logic, < 10 ms response)**:
1. Beam enclosure door switches: Opening any panel → immediate laser shutoff.
2. Vacuum pressure interlock: If source chamber pressure > 50 Pa → laser shuts off (prevents air breakdown).
3. E-stop circuit: Cuts laser power supply and closes beam shutter simultaneously.
4. Coolant flow interlock: If coolant flow < minimum → laser shuts off (prevents thermal damage to beam dumps).

**Beam shutter**: Fast electro-mechanical shutter (response time < 5 ms) in beam path, normally closed, opens only when laser is active and all interlocks are satisfied.

### 4.4 Warning Systems

1. **Warning lights**: Red rotating beacon at each entry point; illuminated when laser is armed or firing.
2. **Audible warning**: Alarm sounds 10 seconds before laser activation.
3. **Warning signs**: ANSI Z535 / ISO 11 standard laser warning signs at all entry points and on the laser enclosure.

---

## 5. Administrative Controls

### 5.1 Laser Safety Officer (LSO)

Designate a qualified Laser Safety Officer responsible for:
- Approving Standard Operating Procedures (SOPs).
- Conducting periodic laser safety training.
- Performing annual safety audits.
- Maintaining laser safety records.

### 5.2 Standard Operating Procedure (SOP)

A written SOP must be created and approved by the LSO before first use. The SOP must include:
1. System description and hazard identification.
2. Required personal protective equipment (PPE).
3. Step-by-step operating procedure.
4. Emergency procedures (eye injury, fire, electrical incident).
5. Maintenance procedures (with laser locked out).

### 5.3 Lockout/Tagout (LOTO)

Before any maintenance inside the beam enclosure:
1. Shut down laser.
2. Verify laser is off (power meter or beam indicator).
3. Close and lock beam shutter.
4. Disconnect high-voltage power supply.
5. Apply lockout tag.
6. Wait 5 minutes for energy storage discharge (capacitor banks).
7. Verify zero energy state with independent measurement.

### 5.4 Training Requirements

All personnel working in the laser area must complete:
- Institutional laser safety training (typically 4–8 hours).
- Site-specific SOP training.
- Eye examination (baseline) and annual follow-up.
- First aid training for laser eye injury.

---

## 6. Emergency Procedures

### 6.1 Laser Eye Injury

1. **Immediately call emergency services** (do not delay for any reason).
2. Do NOT rub the eye.
3. Cover the affected eye with a clean, dry cloth.
4. Transport to ophthalmologist or emergency room immediately.
5. Bring safety data (laser wavelength, power, exposure duration) to the treating physician.

### 6.2 Laser-Induced Fire

1. Activate E-stop (shuts down laser immediately).
2. Sound fire alarm.
3. Evacuate area.
4. Use CO₂ fire extinguisher (not water — electrical equipment present).
5. Call fire department.

### 6.3 Electrical Incident (High Voltage)

1. Do NOT touch the victim if still in contact with electrical source.
2. Disconnect power at the circuit breaker.
3. Call emergency services.
4. Administer CPR if trained and victim is unresponsive.

---

## 7. CO₂ Laser-Specific Hazards

### 7.1 ZnSe Optical Elements

Zinc selenide (ZnSe) windows and lenses used at 10.6 µm are:
- Fragile — handle with care, do not drop.
- Water-soluble (slowly) — wipe with clean, dry optical tissue; do not use water.
- Non-toxic in solid form, but ZnSe dust (if broken) is toxic — vacuum clean, do not inhale.

### 7.2 CO₂ Gas

The laser gain medium may use CO₂/N₂/He gas mixture:
- CO₂ is an asphyxiant at high concentrations (> 5% in air).
- Ensure adequate ventilation in laser room.
- CO₂ detector recommended if laser uses flowing gas (some use sealed-off tubes).

---

## 8. References

1. ANSI Z136.1-2022, *American National Standard for the Safe Use of Lasers*.
2. IEC 60825-1:2014, *Safety of Laser Products — Part 1: Equipment Classification and Requirements*.
3. Laser Institute of America (LIA), *Laser Safety Guide*, 11th ed.
4. OSHA, *Laser Hazards*, [https://www.osha.gov/laser-hazards](https://www.osha.gov/laser-hazards).
5. Rockwell, R.J., *A Review of Laser Accidents*, *J. Laser Appl.* 11, 1999.
