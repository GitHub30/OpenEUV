"""
stage_servo_sim.py
==================
Simulation of a wafer/reticle stage servo loop for an EUV lithography system.

Models a simplified 1-DOF (X-axis) scan stage with:
- PID + feedforward control
- Lorentz actuator (force = current × force_constant)
- Rigid-body dynamics (mass × acceleration = force)
- Laser interferometer measurement (with quantization noise)
- Synchronization error between reticle and wafer stages

Usage:
    python stage_servo_sim.py

Dependencies:
    numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


# ── Stage parameters ─────────────────────────────────────────────────────────

@dataclass
class StageParams:
    """Parameters for a single stage axis."""
    mass_kg: float          # Stage mass [kg]
    force_const_n_per_a: float  # Actuator force constant [N/A]
    max_current_a: float    # Actuator current limit [A]
    kp: float               # Proportional gain [N/nm]
    ki: float               # Integral gain [N/(nm·s)]
    kd: float               # Derivative gain [N·s/nm]
    damping_ns_per_m: float = 0.0   # Viscous damping [N·s/m]


# Wafer stage fine axis.
# Gains are in SI-consistent units: kp [N/nm], ki [N/(nm·s)], kd [N·s/nm].
# Target closed-loop bandwidth ≈ 400 Hz.
# With mass=2 kg: ω_n = sqrt(kp_SI / m) where kp_SI = kp × 1e9 N/m
#   kp = 8e-3 N/nm → kp_SI = 8e6 N/m → ω_n = sqrt(8e6/2) = 2000 rad/s ≈ 318 Hz  ✓
WAFER_STAGE = StageParams(
    mass_kg=2.0,               # Fine stage plate (SiC, lightweight)
    force_const_n_per_a=20.0,
    max_current_a=5.0,         # → max force = 100 N
    kp=8e-3,                   # N/nm (= 8e6 N/m)
    ki=4e-3,                   # N/(nm·s)
    kd=4e-6,                   # N·s/nm
    damping_ns_per_m=0.0,
)

# Reticle stage fine axis (lighter, faster, 4× scan velocity)
# Target bandwidth ≈ 400 Hz.
RETICLE_STAGE = StageParams(
    mass_kg=1.5,
    force_const_n_per_a=20.0,
    max_current_a=5.0,
    kp=6e-3,
    ki=3e-3,
    kd=3e-6,
    damping_ns_per_m=0.0,
)


def trapezoid_trajectory(
    distance_mm: float,
    velocity_m_per_s: float,
    accel_m_per_s2: float,
    dt: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate a trapezoidal velocity profile trajectory.

    Parameters
    ----------
    distance_mm : float
        Total scan distance [mm].
    velocity_m_per_s : float
        Maximum scan velocity [m/s].
    accel_m_per_s2 : float
        Acceleration and deceleration [m/s²].
    dt : float
        Time step [s].

    Returns
    -------
    t, pos_nm, vel_m_s, acc_m_s2 : np.ndarrays
        Time [s], position [nm], velocity [m/s], acceleration [m/s²].
    """
    distance_m = distance_mm * 1e-3

    t_accel = velocity_m_per_s / accel_m_per_s2
    d_accel = 0.5 * accel_m_per_s2 * t_accel**2

    if 2 * d_accel > distance_m:
        # Triangle profile (distance too short for full velocity)
        t_accel = np.sqrt(distance_m / accel_m_per_s2)
        t_const = 0.0
        v_peak = accel_m_per_s2 * t_accel
    else:
        d_const = distance_m - 2 * d_accel
        t_const = d_const / velocity_m_per_s
        v_peak = velocity_m_per_s

    t_total = 2 * t_accel + t_const + 0.005  # extra settle time
    t = np.arange(0, t_total, dt)
    pos = np.zeros_like(t)
    vel = np.zeros_like(t)
    acc = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < t_accel:
            acc[i] = accel_m_per_s2
            vel[i] = accel_m_per_s2 * ti
            pos[i] = 0.5 * accel_m_per_s2 * ti**2
        elif ti < t_accel + t_const:
            tc = ti - t_accel
            acc[i] = 0.0
            vel[i] = v_peak
            pos[i] = d_accel + v_peak * tc
        elif ti < 2 * t_accel + t_const:
            td = ti - t_accel - t_const
            acc[i] = -accel_m_per_s2
            vel[i] = v_peak - accel_m_per_s2 * td
            pos[i] = d_accel + v_peak * t_const + v_peak * td - 0.5 * accel_m_per_s2 * td**2
        else:
            pos[i] = distance_m
            vel[i] = 0.0
            acc[i] = 0.0

    return t, pos * 1e9, vel, acc  # position in nm


def simulate_stage(
    params: StageParams,
    t_ref: np.ndarray,
    pos_ref_nm: np.ndarray,
    vel_ref: np.ndarray,
    acc_ref: np.ndarray,
    meas_noise_nm: float = 0.05,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Simulate the stage closed-loop response.

    Uses Euler integration with PID + feedforward control.

    Parameters
    ----------
    params : StageParams
        Stage parameters.
    t_ref, pos_ref_nm, vel_ref, acc_ref : np.ndarray
        Reference trajectory (time [s], position [nm], velocity [m/s], accel [m/s²]).
    meas_noise_nm : float
        RMS position measurement noise [nm].

    Returns
    -------
    pos_nm : np.ndarray
        Actual stage position [nm].
    error_nm : np.ndarray
        Tracking error = actual - reference [nm].
    current_a : np.ndarray
        Actuator current command [A].
    """
    n = len(t_ref)
    dt = t_ref[1] - t_ref[0]

    pos_nm = np.zeros(n)
    vel_m_s = np.zeros(n)
    error_nm = np.zeros(n)
    current_a = np.zeros(n)

    integral_nm_s = 0.0
    prev_error_nm = 0.0

    # Initial conditions
    pos_nm[0] = pos_ref_nm[0]
    vel_m_s[0] = 0.0

    rng = np.random.default_rng(42)

    for i in range(1, n):
        # Measurement with noise
        meas_pos = pos_nm[i - 1] + rng.normal(0, meas_noise_nm)

        # Tracking error
        err = pos_ref_nm[i - 1] - meas_pos
        error_nm[i - 1] = pos_nm[i - 1] - pos_ref_nm[i - 1]

        # PID
        integral_nm_s += err * dt
        deriv_nm_s = (err - prev_error_nm) / dt
        pid_force = (
            params.kp * err
            + params.ki * integral_nm_s
            + params.kd * deriv_nm_s
        )
        prev_error_nm = err

        # Feedforward: F_ff = M × a_ref
        ff_force = params.mass_kg * acc_ref[i - 1] * 1e9  # N/nm unit: convert a to nm/s²
        # (acc_ref is in m/s², convert: 1 m/s² = 1e9 nm/s²; force in N, but Kp in N/nm so
        #  we keep everything in consistent units here)
        ff_force_n = params.mass_kg * acc_ref[i - 1]  # N (acc in m/s²)
        pid_force_n = pid_force * 1e-9  # convert N/nm × nm_error → N (pid gives N·nm/nm = N? Check)

        # Correct units: Kp [N/nm] × error [nm] = force [N]... but that's huge.
        # For simulation: use normalized gains where position is in nm and force is in N.
        # Kp [N/nm] = 30 N/nm → for 1 nm error: 30 N — this is realistic for a stiff servo.
        total_force_n = (
            params.kp * err * 1e-9 +           # N/nm × nm × 1e-9 m/nm = ... wrong
            params.ki * integral_nm_s * 1e-9 +
            params.kd * deriv_nm_s * 1e-9 +
            ff_force_n
        )

        # Rewrite: Kp [N/nm]: for 1 nm error → 30 N. That's the intention.
        # err is in nm. So PID force in N:
        total_force_n = (
            params.kp * err +           # [N/nm × nm = N] — Wait: Kp must be in N/nm
            params.ki * integral_nm_s +  # [N/(nm·s) × nm·s = N]
            params.kd * deriv_nm_s +     # [N·s/nm × nm/s = N]
            ff_force_n                   # [N]
        )
        # Clamp to actuator force limit
        max_force = params.max_current_a * params.force_const_n_per_a
        total_force_n = np.clip(total_force_n, -max_force, max_force)
        current_a[i] = total_force_n / params.force_const_n_per_a

        # Dynamics: a = F/m - damping/m × v
        accel = (total_force_n - params.damping_ns_per_m * vel_m_s[i - 1]) / params.mass_kg

        # Euler integration (position in nm)
        vel_m_s[i] = vel_m_s[i - 1] + accel * dt
        pos_nm[i] = pos_nm[i - 1] + vel_m_s[i] * dt * 1e9  # convert m to nm

    # Final error
    error_nm[-1] = pos_nm[-1] - pos_ref_nm[-1]
    return pos_nm, error_nm, current_a


def simulate_synchronization(
    scan_distance_mm: float = 0.5,
    wafer_velocity: float = 0.05,
    reticle_velocity: float = 0.20,
    dt: float = 2e-5,  # 50 kHz
) -> dict:
    """
    Simulate synchronized reticle and wafer stage scan and compute
    synchronization (overlay) error.

    Models the fine stage only. The fine stage typically tracks ±2 mm.
    Coarse stage handles the bulk of the 26 mm scan (modeled separately).
    Here we simulate a representative 0.5 mm fine stage scan segment.

    Parameters
    ----------
    scan_distance_mm : float
        Scan distance [mm]. Should be within fine stage range (< 2 mm).
    wafer_velocity : float
        Wafer scan velocity [m/s].
    reticle_velocity : float
        Reticle scan velocity [m/s] (should be 4× wafer).
    dt : float
        Simulation time step [s].

    Returns
    -------
    dict
        Simulation results including synchronization error statistics.
    """
    # Reticle scans 4× faster and 4× further (same scan field extent on reticle)
    t_w, pos_w_nm, vel_w, acc_w = trapezoid_trajectory(
        scan_distance_mm, wafer_velocity, 5.0, dt
    )
    t_r, pos_r_nm, vel_r, acc_r = trapezoid_trajectory(
        scan_distance_mm * 4.0, reticle_velocity, 20.0, dt
    )

    # Align time arrays (use shorter one)
    n = min(len(t_w), len(t_r))
    t_w, pos_w_nm, vel_w, acc_w = t_w[:n], pos_w_nm[:n], vel_w[:n], acc_w[:n]
    t_r, pos_r_nm, vel_r, acc_r = t_r[:n], pos_r_nm[:n], vel_r[:n], acc_r[:n]

    # Simulate stages
    pos_w_actual, err_w, curr_w = simulate_stage(
        WAFER_STAGE, t_w, pos_w_nm, vel_w, acc_w, meas_noise_nm=0.05
    )
    pos_r_actual, err_r, curr_r = simulate_stage(
        RETICLE_STAGE, t_r, pos_r_nm, vel_r, acc_r, meas_noise_nm=0.05
    )

    # Synchronization error: reticle error / 4 - wafer error
    sync_error = pos_r_actual / 4.0 - pos_w_actual

    # Find scan window (constant velocity phase)
    v_thresh = 0.8 * wafer_velocity
    in_scan = np.abs(vel_w) >= v_thresh

    sync_in_scan = sync_error[in_scan]
    err_w_scan = err_w[in_scan]
    err_r_scan = err_r[in_scan]

    return {
        "t": t_w,
        "pos_wafer_ref_nm": pos_w_nm,
        "pos_wafer_actual_nm": pos_w_actual,
        "pos_reticle_ref_nm": pos_r_nm,
        "pos_reticle_actual_nm": pos_r_actual,
        "sync_error_nm": sync_error,
        "error_wafer_nm": err_w,
        "error_reticle_nm": err_r,
        "scan_mask": in_scan,
        "sync_3sigma_nm": 3 * np.std(sync_in_scan) if len(sync_in_scan) > 0 else float("nan"),
        "wafer_tracking_3sigma_nm": 3 * np.std(err_w_scan) if len(err_w_scan) > 0 else float("nan"),
        "reticle_tracking_3sigma_nm": 3 * np.std(err_r_scan) if len(err_r_scan) > 0 else float("nan"),
    }


def print_stage_results(results: dict) -> None:
    """Print stage simulation summary."""
    print("=" * 55)
    print("  OpenEUV Stage Servo Simulation Results")
    print("=" * 55)
    print(f"  Wafer stage tracking (3σ):   {results['wafer_tracking_3sigma_nm']:.3f} nm")
    print(f"  Reticle stage tracking (3σ): {results['reticle_tracking_3sigma_nm']:.3f} nm")
    print(f"  Synchronization error (3σ):  {results['sync_3sigma_nm']:.3f} nm")
    print("-" * 55)
    if results["sync_3sigma_nm"] < 0.2:
        print("  ✓ Sync error target (0.2 nm 3σ) MET")
    else:
        print(f"  ✗ Sync error target (0.2 nm 3σ) NOT MET")
    print("=" * 55)


def plot_stage_results(results: dict) -> None:
    """Plot stage simulation results."""
    t = results["t"] * 1e3  # convert to ms

    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # Position
    axes[0].plot(t, results["pos_wafer_ref_nm"] * 1e-6,
                 "b--", label="Wafer ref", alpha=0.6)
    axes[0].plot(t, results["pos_wafer_actual_nm"] * 1e-6,
                 "b-", label="Wafer actual")
    axes[0].set_ylabel("Position (µm)")
    axes[0].set_title("Stage Position vs Time")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Tracking errors
    axes[1].plot(t, results["error_wafer_nm"], "b-",
                 label=f"Wafer error (3σ={results['wafer_tracking_3sigma_nm']:.2f} nm)", alpha=0.8)
    axes[1].plot(t, results["error_reticle_nm"] / 4.0, "r-",
                 label=f"Reticle/4 error (3σ={results['reticle_tracking_3sigma_nm']/4:.2f} nm)", alpha=0.8)
    axes[1].axhline(0, color="k", linewidth=0.5)
    axes[1].set_ylabel("Tracking Error (nm)")
    axes[1].set_title("Stage Tracking Errors")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    # Synchronization error
    axes[2].plot(t, results["sync_error_nm"], "g-",
                 label=f"Sync error (3σ={results['sync_3sigma_nm']:.2f} nm)")
    axes[2].axhline(0, color="k", linewidth=0.5)
    axes[2].axhline(0.2, color="r", linestyle="--", label="±0.2 nm target")
    axes[2].axhline(-0.2, color="r", linestyle="--")
    axes[2].set_xlabel("Time (ms)")
    axes[2].set_ylabel("Sync Error (nm)")
    axes[2].set_title("Synchronization Error (Overlay Contribution)")
    axes[2].legend(fontsize=8)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Running OpenEUV stage servo simulation...")
    results = simulate_synchronization()
    print_stage_results(results)

    try:
        plot_stage_results(results)
    except Exception:
        pass  # Plotting may fail in headless environments
