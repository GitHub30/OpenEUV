"""
collector_efficiency.py
=======================
Ray-trace model of an ellipsoidal EUV collector mirror.
Computes collection efficiency as a function of numerical aperture,
debris mitigation (foil trap), and mirror reflectance.

Usage:
    python collector_efficiency.py

Dependencies:
    numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt


def solid_angle_fraction(theta_min_deg: float, theta_max_deg: float) -> float:
    """
    Compute the fraction of 4π sr subtended by a cone defined by
    half-angles theta_min and theta_max from the optical axis.

    Parameters
    ----------
    theta_min_deg : float
        Inner half-angle in degrees (for central obstruction).
    theta_max_deg : float
        Outer half-angle in degrees (maximum collection angle).

    Returns
    -------
    float
        Solid angle fraction of 4π sr (dimensionless, 0–1).
    """
    theta_min = np.radians(theta_min_deg)
    theta_max = np.radians(theta_max_deg)
    omega = 2 * np.pi * (np.cos(theta_min) - np.cos(theta_max))
    return omega / (4 * np.pi)


def collector_euv_throughput(
    source_power_w: float,
    theta_min_deg: float,
    theta_max_deg: float,
    reflectance: float,
    foil_trap_transmission: float = 1.0,
    ils_transmission: float = 1.0,
) -> dict:
    """
    Compute EUV power budget from source to intermediate focus (IF)
    and through the illumination system.

    Parameters
    ----------
    source_power_w : float
        In-band EUV power emitted into 2π sr [W].
    theta_min_deg : float
        Collector inner (obstruction) half-angle [degrees].
    theta_max_deg : float
        Collector outer half-angle [degrees].
    reflectance : float
        Mo/Si multilayer peak reflectance (0–1).
    foil_trap_transmission : float, optional
        Foil trap / rotating foil trap EUV transmission (0–1). Default 1.0 (no foil trap).
    ils_transmission : float, optional
        Total illumination system (ILS) EUV transmission (0–1). Default 1.0.

    Returns
    -------
    dict
        Power at each stage in watts.
    """
    # Source emits into 2π sr → multiply by 2 for full 4π
    # Convention: source_power_w is power into 2π (half-space toward collector)
    f_collect = solid_angle_fraction(theta_min_deg, theta_max_deg)
    # Scale to 2π hemisphere (source emits into 2π sr toward collector)
    # solid_angle_fraction gives fraction of 4π, and source emits into 2π (upper hemisphere)
    # so effective collection = f_collect * 4π / 2π = 2 * f_collect
    f_collect_2pi = min(2.0 * f_collect, 1.0)

    p_collected = source_power_w * f_collect_2pi
    p_after_mirror = p_collected * reflectance
    p_after_foil = p_after_mirror * foil_trap_transmission
    p_at_if = p_after_foil
    p_at_reticle = p_at_if * ils_transmission

    return {
        "source_2pi_W": source_power_w,
        "collection_fraction": f_collect_2pi,
        "collected_W": p_collected,
        "after_mirror_W": p_after_mirror,
        "after_foil_trap_W": p_after_foil,
        "at_IF_W": p_at_if,
        "at_reticle_W": p_at_reticle,
    }


def lpp_source_power(
    laser_power_w: float, conversion_efficiency: float
) -> float:
    """
    Estimate in-band EUV power at 13.5 nm from an LPP source.

    Parameters
    ----------
    laser_power_w : float
        CO₂ drive laser average power [W].
    conversion_efficiency : float
        Laser-to-EUV conversion efficiency into 2π sr, 13.5 nm ±1% (0–1).

    Returns
    -------
    float
        In-band EUV power emitted into 2π sr [W].
    """
    return laser_power_w * conversion_efficiency


def plot_power_budget(
    laser_powers_kw: list[float],
    ce: float = 0.05,
    theta_min_deg: float = 6.0,
    theta_max_deg: float = 60.0,
    reflectance: float = 0.67,
    foil_trap_t: float = 0.40,
    ils_t: float = 0.137,
) -> None:
    """
    Plot EUV power at IF and at reticle as a function of drive laser power.

    Parameters
    ----------
    laser_powers_kw : list of float
        Drive laser average power values to sweep [kW].
    ce : float
        Conversion efficiency (default 5%).
    theta_min_deg : float
        Collector inner half-angle [degrees].
    theta_max_deg : float
        Collector outer half-angle [degrees].
    reflectance : float
        Collector mirror reflectance.
    foil_trap_t : float
        Foil trap transmission.
    ils_t : float
        ILS transmission.
    """
    if_powers = []
    reticle_powers = []

    for p_kw in laser_powers_kw:
        source_p = lpp_source_power(p_kw * 1e3, ce)
        budget = collector_euv_throughput(
            source_p, theta_min_deg, theta_max_deg,
            reflectance, foil_trap_t, ils_t
        )
        if_powers.append(budget["at_IF_W"])
        reticle_powers.append(budget["at_reticle_W"])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(laser_powers_kw, if_powers, "b-o", label="Power at IF")
    ax.plot(laser_powers_kw, reticle_powers, "r-s", label="Power at reticle")
    ax.axhline(250, color="k", linestyle="--", label="250 W IF target")
    ax.set_xlabel("CO₂ Drive Laser Power (kW)")
    ax.set_ylabel("EUV Power (W)")
    ax.set_title(
        f"EUV Power Budget\n"
        f"CE={ce*100:.0f}%, θ_max={theta_max_deg}°, R_coll={reflectance:.0%}, "
        f"Foil={foil_trap_t:.0%}, ILS={ils_t:.0%}"
    )
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(if_powers) * 1.2)
    plt.tight_layout()
    plt.show()


def print_detailed_budget(
    laser_power_kw: float = 30.0,
    ce: float = 0.05,
    theta_min_deg: float = 6.0,
    theta_max_deg: float = 60.0,
    reflectance: float = 0.67,
    foil_trap_t: float = 0.40,
    ils_t: float = 0.137,
) -> None:
    """Print a detailed EUV power budget table."""
    source_p = lpp_source_power(laser_power_kw * 1e3, ce)
    budget = collector_euv_throughput(
        source_p, theta_min_deg, theta_max_deg,
        reflectance, foil_trap_t, ils_t
    )
    f = solid_angle_fraction(theta_min_deg, theta_max_deg)

    print("=" * 55)
    print("  OpenEUV EUV Power Budget")
    print("=" * 55)
    print(f"  Drive laser power:          {laser_power_kw:.1f} kW")
    print(f"  Conversion efficiency:      {ce*100:.1f}%")
    print(f"  θ_min / θ_max:              {theta_min_deg}° / {theta_max_deg}°")
    print(f"  Collector solid angle:      {f*4*np.pi:.3f} sr = {f*100:.1f}% of 4π")
    print(f"  Collection fraction (2π):   {budget['collection_fraction']*100:.1f}%")
    print(f"  Mirror reflectance:         {reflectance*100:.0f}%")
    print(f"  Foil trap transmission:     {foil_trap_t*100:.0f}%")
    print(f"  ILS transmission:           {ils_t*100:.1f}%")
    print("-" * 55)
    print(f"  Source power (2π sr):       {budget['source_2pi_W']:.1f} W")
    print(f"  Collected by mirror:        {budget['collected_W']:.1f} W")
    print(f"  After mirror reflection:    {budget['after_mirror_W']:.1f} W")
    print(f"  After foil trap:            {budget['after_foil_trap_W']:.1f} W")
    print(f"  At intermediate focus:      {budget['at_IF_W']:.1f} W")
    print(f"  At reticle (after ILS):     {budget['at_reticle_W']:.1f} W")
    print("=" * 55)
    if budget["at_IF_W"] >= 250:
        print("  ✓ IF power target (250 W) MET")
    else:
        shortfall = 250 - budget["at_IF_W"]
        print(f"  ✗ IF power target (250 W) NOT MET by {shortfall:.1f} W")
    print()


if __name__ == "__main__":
    # Print a detailed budget for the nominal design point
    print_detailed_budget(
        laser_power_kw=30.0,
        ce=0.05,
        theta_min_deg=6.0,
        theta_max_deg=60.0,
        reflectance=0.67,
        foil_trap_t=0.40,
        ils_t=0.137,
    )

    # Also show a case without foil trap (debris mitigated by H₂ + magnetic)
    print("--- Case: No foil trap (debris mitigation by H₂ + magnetic) ---")
    print_detailed_budget(
        laser_power_kw=30.0,
        ce=0.05,
        theta_min_deg=6.0,
        theta_max_deg=60.0,
        reflectance=0.67,
        foil_trap_t=1.0,  # no foil trap
        ils_t=0.137,
    )

    # Sweep laser power
    powers = np.linspace(10, 50, 41).tolist()
    print("Laser power sweep (no foil trap):")
    print(f"{'Laser (kW)':>12}  {'IF power (W)':>14}  {'Reticle (W)':>13}")
    print("-" * 44)
    for p in [10, 20, 30, 40, 50]:
        s = lpp_source_power(p * 1e3, 0.05)
        b = collector_euv_throughput(s, 6.0, 60.0, 0.67, 1.0, 0.137)
        print(f"{p:>12.0f}  {b['at_IF_W']:>14.1f}  {b['at_reticle_W']:>13.1f}")

    # Plot (optional, requires matplotlib)
    try:
        plot_power_budget(powers, ce=0.05, foil_trap_t=1.0)
    except Exception:
        pass  # Plotting may fail in headless environments
