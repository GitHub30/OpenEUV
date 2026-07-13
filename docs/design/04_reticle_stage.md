# Reticle Stage — Detailed Design

## 1. Overview

The reticle stage holds and scans the EUV reflective mask (reticle) at velocities up to 1.5 m/s with dynamic overlay contribution < 0.3 nm (3σ). Because EUV reticles are reflective (not transmissive), the stage must also accommodate the illumination beam path impinging from above and the EUV beam reflecting upward into the projection optics.

---

## 2. EUV Reticle Overview

### 2.1 Construction

| Layer | Material | Thickness | Function |
|---|---|---|---|
| Substrate | LTEM glass (low TIR) | 6.35 mm | Mechanical support |
| ML coating (back) | Mo/Si, 40 bilayers | ~280 nm | EUV reflector |
| Buffer layer | Ru or SiO₂ | 2.5 nm | Absorber etch stop |
| Absorber | TaN or TaBN | 70–80 nm | Pattern definition |
| Capping | TiO₂ or SiO₂ | 5 nm | Chemical protection |

### 2.2 Reticle Standard

- Size: 152 mm × 152 mm × 6.35 mm (SEMI P38 standard).
- Flatness: < 50 nm (back surface, after chucking).
- Cleanliness: ISO Class 1 (≤ 1 particle/m² > 100 nm) before use.

---

## 3. Stage Architecture

### 3.1 Overview

```
Reticle (152×152 mm)
    └── Electrostatic chuck (ESC)
            └── Fine stage (6-DOF Lorentz actuators)
                    └── Coarse stage (linear motors, X-Y travel ~250 mm)
                            └── Guideway (air bearing on granite base)
                                    └── Metrology frame (vibration-isolated)
```

### 3.2 Degrees of Freedom

| DOF | Actuator | Sensor | Range |
|---|---|---|---|
| X (scan) | Linear motor (coarse) + Lorentz (fine) | Laser interferometer | ±130 mm |
| Y (step) | Linear motor (coarse) + Lorentz (fine) | Laser interferometer | ±130 mm |
| Z | 3 × voice coil (fine) | Capacitance | ±0.5 mm |
| Rx (tip) | Differential Z | Capacitance | ±1 mrad |
| Ry (tilt) | Differential Z | Capacitance | ±1 mrad |
| Rz (rotation) | Differential X/Y fine | Laser interferometer | ±2 mrad |

---

## 4. Coarse Stage

### 4.1 Linear Motor

- **Type**: Three-phase linear induction motor (ironless, to avoid cogging).
- **Peak force**: 2000 N.
- **Continuous force**: 500 N.
- **Maximum velocity**: 2.0 m/s.
- **Maximum acceleration**: 50 m/s².
- **Stroke**: ±150 mm (X), ±150 mm (Y).

### 4.2 Air Bearing Guideway

- **Type**: Porous carbon or orifice-compensated air bearings.
- **Stiffness**: ≥ 200 N/µm per bearing pad.
- **Load capacity**: ≥ 500 N per pad.
- **Air supply**: Ultra-dry, filtered nitrogen or clean air at 4–6 bar.
- **Base material**: Grade A granite (thermal expansion 5–7 µm/m·K); isothermalized at 22°C.

### 4.3 Reaction Force Cancellation

The stage motor reaction force disturbs the machine base and couples to the wafer stage, degrading overlay. Options:
1. **Balance mass**: A counter-moving mass equal to stage mass; absorbs reaction force.
2. **Force frame**: Rigid force loop connecting stage and reticle; isolates reaction forces from metrology frame.

---

## 5. Fine Stage

### 5.1 Lorentz Actuators

- **Number**: 6 (3 horizontal for X-Y-Rz, 3 vertical for Z-Rx-Ry).
- **Type**: Moving-coil voice coil actuators with permanent magnet stators.
- **Force constant**: 10–20 N/A.
- **Current range**: ±5 A.
- **Peak force**: ±100 N per actuator.
- **Stroke**: ±2 mm (X/Y), ±0.5 mm (Z).

### 5.2 Fine Stage Mass and Stiffness

- **Target mass**: < 5 kg (minimizes required actuator force for given acceleration).
- **Material**: Silicon carbide (SiC) or CFRP plate.
- **First resonance**: ≥ 200 Hz (critical: control bandwidth must be well below this).

---

## 6. Electrostatic Chuck

### 6.1 Purpose

Clamp the reticle flat against the chuck surface to achieve ≤ 50 nm flatness in the EUV beam path, compensating for reticle backside non-flatness.

### 6.2 Design

- **Type**: Bipolar electrostatic chuck (alternating high-voltage electrodes).
- **Operating voltage**: 1000–3000 V (alternating polarity electrodes).
- **Clamping pressure**: ~5 kPa (adequate for non-contact operation in vacuum).
- **Chuck material**: Zerodur® or SiC with thin insulating layer (Al₂O₃, ALD-deposited).
- **Flatness specification**: ≤ 30 nm (unloaded chuck surface).
- **Protrusions (mesas)**: Three-point kinematic support protrusions, 0.3 mm diameter, 10–20 µm height, to define contact plane.

### 6.3 Thermal Control

- Embedded thin-film heaters and Peltier coolers maintain chuck at 22.000 ± 0.020°C.
- Feedback: Pt100 RTD sensors at 4 locations.

---

## 7. Metrology

### 7.1 Laser Interferometer

- **Type**: Heterodyne, dual-axis, Zeeman-stabilized HeNe laser.
- **Wavelength**: 632.8 nm.
- **Resolution**: ≤ 0.1 nm (after interpolation).
- **Measurement axes**: X, Y, Rz (3 interferometer beams minimum).
- **Reference mirror**: Zerodur® flat mirror bonded to metrology frame.

### 7.2 Abbe Error

Laser interferometer measures position at a point offset from the actual reticle surface. Abbe error = angular error × arm length. Design goal:
```
Abbe arm (Z offset) < 5 mm
Angular error < 0.1 µrad (from Rz interferometer)
Abbe error < 5 mm × 0.1 µrad = 0.5 nm — acceptable
```

---

## 8. Control System

### 8.1 Servo Loop

```
Scan trajectory → Feedforward (force model) + PID feedback → Motor current → Stage position
Stage position ← Laser interferometer ← (sampled at 50 kHz)
```

**Control bandwidth**: 150 Hz (fine stage), 80 Hz (coarse stage).

### 8.2 Trajectory Profile

For a typical scan (26 mm slit, 1.5 m/s scan velocity):
```
Acceleration phase: 40 m/s² for 37.5 ms → 1.5 m/s
Constant velocity phase: 26 mm / 1.5 m/s ≈ 17.3 ms
Deceleration phase: 37.5 ms
Total scan time: ~92 ms per field
```

### 8.3 Synchronization with Wafer Stage

The reticle stage must scan at exactly 4× the wafer stage velocity (due to 4× demagnification). Synchronization is maintained by a real-time FPGA controller reading both interferometers at 50 kHz and commanding both stages simultaneously.

Synchronization error budget: < 0.2 nm rms (after feedforward correction).

---

## 9. References

1. H. Butler, "Position control in lithographic equipment," *IEEE Control Syst. Mag.* 31, 2011.
2. J. van Schoot et al., "EUV lithography scanner for sub-8 nm resolution," *Proc. SPIE* 10143, 2017.
3. R. Munnig Schmidt et al., *The Design of High Performance Mechatronics*, Delft University Press, 2014.
