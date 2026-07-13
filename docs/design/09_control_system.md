# Control System — Detailed Design

## 1. Overview

The control system coordinates all subsystems of the EUV lithography tool to achieve specified throughput (≥ 125 wph) and accuracy (overlay < 1.5 nm, CD uniformity < 1%). It spans from nanosecond-level laser pulse timing to hour-level job scheduling.

---

## 2. Control Hierarchy

### 2.1 Levels

```
Level 3 ─ Supervisory Controller (Host PC)
           ├── Job scheduler and recipe manager
           ├── Subsystem health monitoring
           ├── Alarm and interlock manager (non-safety)
           ├── Data logging and SPC
           └── User interface (HMI)

Level 2 ─ Sequence Controller (Real-Time PC)
           ├── Scan sequence coordination
           ├── Wafer and reticle exchange sequence
           ├── Interlock enforcement
           └── Subsystem-level state machines

Level 1 ─ Servo Controllers (FPGA + DSP)
           ├── Wafer stage X/Y/Z servo (50 kHz)
           ├── Reticle stage X/Y/Z servo (50 kHz)
           ├── Laser power control (50 kHz)
           ├── Vacuum control (PLC, 100 Hz)
           └── Temperature control (PID loops, 10 Hz)

Level 0 ─ Hardware (Sensors, Actuators, Drives)
```

---

## 3. Stage Servo Design

### 3.1 Control Loop Structure

```
                    ┌──────────────────────────────────┐
Position reference  │   Feedforward (inverse dynamics)  │  Force command
────────────────────┼──────────────────────────────────┼──────────────────▶
                    │                                   │
          ┌─────────┼──────────┐                       │
          │    PID controller  │                       │
          └─────────────────────┘                       │
                    ▲                                    │
          Position measurement (laser interferometer)   │
          ←─────────────────────────────────────────────┘
```

### 3.2 Feedforward Design

Model-based feedforward reduces tracking error by predicting required force from the trajectory:

```
F_ff = M_stage × a_ref + B × v_ref + K_spring × x_ref
where:
    M_stage = stage mass (measured by system ID)
    B = damping coefficient (measured)
    K_spring = spring stiffness from cables/hoses (measured)
    a_ref, v_ref, x_ref = reference acceleration, velocity, position
```

### 3.3 PID Tuning

```python
# Discrete-time PID (Tustin approximation, fs = 50 kHz)
def pid_update(error, prev_error, integral, Kp, Ki, Kd, dt):
    integral += error * dt
    derivative = (error - prev_error) / dt
    output = Kp * error + Ki * integral + Kd * derivative
    return output, integral

# Typical wafer stage gains:
# Kp = 50 N/nm, Ki = 100 N/(nm·s), Kd = 0.5 N·s/nm
# Bandwidth: ~400 Hz (fine stage), ~100 Hz (coarse stage)
```

### 3.4 Anti-Windup

Integrator windup occurs when the actuator saturates. Use back-calculation anti-windup:
```
integral += Ki * dt * error - Ka * dt * (output_sat - output_unsat)
where Ka = 1/Ti (anti-windup gain)
```

### 3.5 Notch Filters

Structural resonances can excite stage vibrations. Add notch filters at resonance frequencies:
```
H_notch(z) = (1 - 2cos(ω_n T_s)z⁻¹ + z⁻²) / (1 - 2r·cos(ω_n T_s)z⁻¹ + r²·z⁻²)
where:
    ω_n = resonance frequency (rad/s)
    T_s = 1/50000 s (sample period)
    r = 0.9 (pole radius, controls notch bandwidth)
```

---

## 4. Scan Synchronization

### 4.1 Synchronization Requirement

The reticle stage scans at 4× the wafer stage velocity (4:1 synchronization ratio). Synchronization error appears directly as overlay error:

```
Overlay_x = ΔX_reticle / 4 - ΔX_wafer  (reticle error / demagnification - wafer error)
Target: RSS contribution < 0.2 nm rms
```

### 4.2 FPGA Synchronization

Both stage servo loops run on the same FPGA clock (50 MHz). Trajectory generation for both stages uses the same timestamp:

```vhdl
-- FPGA pseudo-code for synchronized trajectory generation
process(clk_50MHz)
begin
    if rising_edge(clk_50MHz) then
        tick_counter <= tick_counter + 1;
        if tick_counter = 1000 then  -- 50 kHz update
            tick_counter <= 0;
            -- Generate reticle position reference
            x_ref_reticle <= trajectory_reticle(scan_time);
            -- Generate wafer position reference (4× slower)
            x_ref_wafer <= trajectory_wafer(scan_time);
            scan_time <= scan_time + dt;
        end if;
    end if;
end process;
```

### 4.3 Cross-Coupling Correction

Floor vibrations and air flows can perturb both stages. A cross-coupling feedforward adds a correction to each stage based on the measured position error of the other:

```
F_ff_wafer += K_coupling × (x_reticle_error / 4 - x_wafer_error)
```

---

## 5. Laser Dose Control

### 5.1 Dose Uniformity Requirement

Dose non-uniformity causes critical dimension (CD) variation:
```
CD/CD₀ ≈ 1 + n × (Dose - Dose₀) / Dose₀
where n = process sensitivity (typically n = 3–6 for EUV resists)

CD uniformity budget: < 0.5% (3σ)
→ Dose uniformity: < 0.1% (3σ) (for n = 5)
```

### 5.2 Dose Control Algorithm

```python
def dose_control(target_dose, scan_velocity, slit_area, 
                 euv_power_measured, pulse_count):
    """
    Control EUV dose by adjusting scan velocity or laser power.
    
    dose_delivered = integral(P_EUV / (scan_vel × slit_width)) dt
    
    Strategy: Fixed scan velocity, vary source power via laser timing/energy.
    """
    dose_per_pulse = euv_power_measured / (scan_velocity * slit_area * 50000)
    cumulative_dose = dose_per_pulse * pulse_count
    dose_error = target_dose - cumulative_dose
    
    # Adjust: small velocity correction
    velocity_correction = -dose_error * Kv
    return velocity_correction
```

### 5.3 EUV Power Monitor

- **Sensor**: EUV photodiode (silicon PIN diode with thin SiO₂ window, ~100 nm thick).
- **Location**: Near intermediate focus (IF), monitoring ~0.1% of total EUV power.
- **Bandwidth**: > 50 kHz (one reading per pulse).
- **Calibration**: NIST-traceable EUV radiometer calibration every 6 months.

---

## 6. Interlock and Safety System

### 6.1 Safety Interlocks (Hardware)

Hardware interlocks operate independently of software:
- CO₂ laser beam shutoff triggered by: enclosure door open, vacuum pressure loss, E-stop.
- High-voltage shutoff triggered by: enclosure door open, E-stop.
- H₂ gas shutoff triggered by: H₂ concentration alarm, E-stop.

Hardware interlock chain uses relay logic (no software in the path) with < 10 ms response time.

### 6.2 Software Interlocks

Software interlocks for non-safety-critical events:
- Vacuum pressure out of range → pause operation, alert operator.
- Stage position error > threshold → stop scan, retry.
- Laser power drift > 5% → recalibrate source, alert.
- Temperature out of range → pause, alert.

### 6.3 State Machine

```
SYSTEM STATES:
    IDLE → INITIALIZING → VACUUM_READY → SOURCE_READY → ALIGNMENT
    → EXPOSING → WAFER_EXCHANGE → [back to ALIGNMENT or IDLE]
    
Any state → FAULT → FAULT_RECOVERY → previous state or IDLE
Any state → E_STOP → SAFE_STATE (all power off, vents closed)
```

---

## 7. Software Architecture

### 7.1 Real-Time Layer (FPGA)

| Module | Function | Update Rate |
|---|---|---|
| Stage servo (wafer) | PID + feedforward, interferometer read | 50 kHz |
| Stage servo (reticle) | PID + feedforward, interferometer read | 50 kHz |
| Laser timing | Pulse trigger, energy measurement | 50 kHz |
| I/O management | Sensor data aggregation | 50 kHz |

**Implementation**: Xilinx Zynq-7000 (ARM + FPGA) or equivalent.
- FPGA logic: VHDL/Verilog for deterministic I/O and servo loops.
- ARM processor: RTOS (FreeRTOS or Xenomai) for sequencing.

### 7.2 Sequence Controller Layer (Real-Time Linux)

- **OS**: Ubuntu 22.04 LTS with PREEMPT_RT patch (jitter < 50 µs).
- **Language**: C++ with Boost.Asio for async I/O.
- **Communication to FPGA**: PCIe or EtherCAT.
- **Communication to supervisory**: ZeroMQ or ROS2.

### 7.3 Supervisory Layer (Host PC)

- **OS**: Ubuntu 22.04 LTS (or Windows 11).
- **Language**: Python 3.10+ with asyncio.
- **GUI**: Qt5 (PyQt) or web-based React frontend.
- **Database**: InfluxDB (time-series data), PostgreSQL (recipes, wafer history).
- **Visualization**: Grafana for real-time dashboards.
- **Recipe format**: YAML with JSON Schema validation.

### 7.4 Data Flow

```
Sensors (50 kHz) → FPGA ring buffer → Sequence controller (decimated, 1 kHz)
    → Supervisory controller (100 Hz) → InfluxDB → Grafana dashboard
    → Operator display (1 Hz human-readable)

Critical alarms: hardware interlock chain (< 10 ms) bypasses all software
```

---

## 8. Control System Commissioning

### 8.1 Stage Identification

1. Measure stage frequency response (chirp signal, 1–1000 Hz) with FFT analysis.
2. Identify model parameters (mass, stiffness, damping, resonances).
3. Tune PID and feedforward gains.
4. Verify bandwidth and phase margin (bandwidth ≥ 400 Hz, phase margin ≥ 45°).

### 8.2 Overlay Calibration

1. Print overlay targets at multiple doses and focus settings.
2. Measure overlay with off-line tool (CD-SEM or optical overlay).
3. Decompose overlay error into systematic components (translation, rotation, magnification).
4. Enter correction tables into recipe.
5. Verify residual overlay < 1.0 nm (3σ).

---

## 9. References

1. H. Butler, "Position control in lithographic equipment," *IEEE Control Syst. Mag.* 31, 2011.
2. R. Munnig Schmidt et al., *The Design of High Performance Mechatronics*, Delft University Press, 2014.
3. M. Steinbuch, "Repetitive control for systems with uncertain period-time," *Automatica* 38, 2002.
4. G. Goodwin et al., *Control System Design*, Prentice Hall, 2001.
