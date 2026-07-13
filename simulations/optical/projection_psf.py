"""
projection_psf.py
=================
Simplified point spread function (PSF) and imaging performance model
for a 6-mirror EUV projection optics system at NA = 0.33, λ = 13.5 nm.

This module uses scalar diffraction theory (Hopkins / Abbe imaging) to:
- Compute the diffraction-limited PSF.
- Compute the optical transfer function (OTF) and modulation transfer function (MTF).
- Estimate Strehl ratio from wavefront RMS error.
- Estimate resolution at various k₁ factors.

Usage:
    python projection_psf.py

Dependencies:
    numpy, scipy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


# ── Physical constants ──────────────────────────────────────────────────────
WAVELENGTH_NM = 13.5          # EUV wavelength [nm]
WAVELENGTH_M = 13.5e-9        # EUV wavelength [m]
NA = 0.33                     # Image-side numerical aperture
DEMAGNIFICATION = 4           # 4× reduction system


def airy_psf(
    na: float,
    wavelength_nm: float,
    grid_nm: float = 5.0,
    grid_size: int = 256,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the Airy disk (diffraction-limited PSF) for a circular aperture.

    Parameters
    ----------
    na : float
        Numerical aperture of the imaging system.
    wavelength_nm : float
        Wavelength in nanometers.
    grid_nm : float
        Pixel size in the image plane [nm]. Default 5 nm.
    grid_size : int
        Number of pixels per side. Default 256.

    Returns
    -------
    psf : np.ndarray
        Normalized 2D PSF array (peak = 1).
    x_nm : np.ndarray
        1D coordinate array [nm] (both axes are equal).
    """
    half = grid_size // 2
    x_nm = (np.arange(grid_size) - half) * grid_nm
    X, Y = np.meshgrid(x_nm, x_nm)
    R = np.sqrt(X**2 + Y**2)

    # Airy disk: PSF ~ (2 J1(u) / u)² where u = π × r × NA / λ
    from scipy.special import j1
    u = np.pi * R * na / wavelength_nm
    # Avoid division by zero at center
    with np.errstate(invalid="ignore", divide="ignore"):
        airy = np.where(u == 0, 1.0, (2 * j1(u) / u) ** 2)
    airy /= airy.max()
    return airy, x_nm


def coherent_otf(
    na: float,
    wavelength_nm: float,
    grid_size: int = 256,
    partial_coherence: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the Optical Transfer Function (OTF) for a diffraction-limited system.

    For fully coherent illumination (σ = 0):
        OTF = 1 for f < f_cutoff, 0 otherwise (top-hat pupil).
    For incoherent illumination (σ → ∞):
        OTF = (2/π) × (arccos(f/f_c) - (f/f_c)×√(1-(f/f_c)²)) for f < 2 f_c.

    Parameters
    ----------
    na : float
        Numerical aperture.
    wavelength_nm : float
        Wavelength in nm.
    grid_size : int
        Number of frequency points.
    partial_coherence : float
        Partial coherence factor σ (0 = coherent, large = incoherent).
        Only 0 and "incoherent" (σ→∞) are implemented here.

    Returns
    -------
    mtf : np.ndarray
        Modulation Transfer Function (|OTF|) vs. spatial frequency.
    freq_cycles_per_nm : np.ndarray
        Spatial frequency axis [cycles/nm].
    """
    f_cutoff = na / wavelength_nm  # cycles/nm (coherent cutoff)
    f_incoherent_cutoff = 2 * f_cutoff  # incoherent cutoff

    freq = np.linspace(0, f_incoherent_cutoff * 1.1, grid_size)

    if partial_coherence == 0:
        # Fully coherent: step function at f_cutoff
        mtf = np.where(freq <= f_cutoff, 1.0, 0.0).astype(float)
    else:
        # Fully incoherent: diffraction-limited MTF
        f_norm = freq / f_incoherent_cutoff
        with np.errstate(invalid="ignore"):
            mtf = (2 / np.pi) * (
                np.arccos(np.clip(f_norm, 0, 1))
                - np.clip(f_norm, 0, 1) * np.sqrt(np.maximum(1 - f_norm**2, 0))
            )
        mtf = np.clip(mtf, 0, 1)

    return mtf, freq


def strehl_from_wavefront_rms(wfe_rms_nm: float, wavelength_nm: float) -> float:
    """
    Estimate Strehl ratio from wavefront RMS error using the Maréchal approximation.

    Valid for Strehl > 0.5 (mild aberrations):
        S ≈ exp(-(2π × W_rms / λ)²)

    Parameters
    ----------
    wfe_rms_nm : float
        Wavefront RMS error [nm].
    wavelength_nm : float
        Wavelength [nm].

    Returns
    -------
    float
        Estimated Strehl ratio (0–1).
    """
    phase_rms = 2 * np.pi * wfe_rms_nm / wavelength_nm  # radians
    return float(np.exp(-(phase_rms**2)))


def resolution_half_pitch(
    k1: float, na: float, wavelength_nm: float
) -> float:
    """
    Compute resolution half-pitch using the Rayleigh-k1 formula.

    Parameters
    ----------
    k1 : float
        Process factor (0.25 = theoretical minimum for coherent, 0.61 = Rayleigh).
    na : float
        Numerical aperture.
    wavelength_nm : float
        Wavelength [nm].

    Returns
    -------
    float
        Half-pitch resolution [nm].
    """
    return k1 * wavelength_nm / na


def depth_of_focus(k2: float, na: float, wavelength_nm: float) -> float:
    """
    Compute depth of focus (one-sided, ±DOF).

    Parameters
    ----------
    k2 : float
        DOF process factor (0.5 = Rayleigh).
    na : float
        Numerical aperture.
    wavelength_nm : float
        Wavelength [nm].

    Returns
    -------
    float
        One-sided depth of focus [nm].
    """
    return k2 * wavelength_nm / (na**2)


def print_performance_summary(
    na: float = NA,
    wavelength_nm: float = WAVELENGTH_NM,
    wfe_rms_nm: float = 0.96,
) -> None:
    """Print imaging performance summary for an EUV projection system."""
    print("=" * 55)
    print("  OpenEUV Projection Optics Performance")
    print("=" * 55)
    print(f"  Wavelength:                 {wavelength_nm:.1f} nm")
    print(f"  Numerical aperture (NA):    {na:.2f}")
    print(f"  Demagnification:            {DEMAGNIFICATION}×")
    print("-" * 55)

    for k1, label in [(0.61, "Rayleigh"), (0.40, "Practical DUV"), (0.32, "With PSM/OPC")]:
        hp = resolution_half_pitch(k1, na, wavelength_nm)
        print(f"  k₁={k1:.2f} ({label:<18}): {hp:.1f} nm HP")

    print()
    for k2, label in [(0.5, "Rayleigh"), (0.7, "Process-enhanced")]:
        dof = depth_of_focus(k2, na, wavelength_nm)
        print(f"  k₂={k2:.1f} DOF ({label:<20}): ±{dof:.0f} nm")

    print()
    strehl = strehl_from_wavefront_rms(wfe_rms_nm, wavelength_nm)
    print(f"  Wavefront RMS:              {wfe_rms_nm:.2f} nm (λ/{wavelength_nm/wfe_rms_nm:.0f})")
    print(f"  Strehl ratio (Maréchal):    {strehl:.4f}")
    print(f"  Coherent cutoff:            {na/wavelength_nm*1000:.2f} cycles/µm")
    print(f"  Incoherent cutoff:          {2*na/wavelength_nm*1000:.2f} cycles/µm")
    print("=" * 55)


def plot_mtf(
    na: float = NA,
    wavelength_nm: float = WAVELENGTH_NM,
) -> None:
    """Plot coherent and incoherent MTF curves."""
    mtf_coherent, freq_c = coherent_otf(na, wavelength_nm, partial_coherence=0)
    mtf_incoherent, freq_i = coherent_otf(na, wavelength_nm, partial_coherence=1)

    # Convert cycles/nm to cycles/µm
    freq_c_um = freq_c * 1e3
    freq_i_um = freq_i * 1e3

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(freq_c_um, mtf_coherent, "b-", label="Coherent (σ=0)", linewidth=2)
    ax.plot(freq_i_um, mtf_incoherent, "r--", label="Incoherent (σ→∞)", linewidth=2)
    ax.axvline(na / wavelength_nm * 1e3, color="b", alpha=0.3, linestyle=":")
    ax.axvline(2 * na / wavelength_nm * 1e3, color="r", alpha=0.3, linestyle=":")
    ax.set_xlabel("Spatial Frequency (cycles/µm)")
    ax.set_ylabel("MTF")
    ax.set_title(f"EUV MTF — NA={na}, λ={wavelength_nm} nm")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 2 * na / wavelength_nm * 1e3 * 1.1)
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    plt.show()


def plot_psf(
    na: float = NA,
    wavelength_nm: float = WAVELENGTH_NM,
) -> None:
    """Plot the diffraction-limited Airy disk PSF."""
    psf, x = airy_psf(na, wavelength_nm, grid_nm=1.0, grid_size=128)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 2D PSF
    im = axes[0].imshow(
        psf,
        extent=[x[0], x[-1], x[0], x[-1]],
        cmap="hot",
        origin="lower",
        vmin=0, vmax=1,
    )
    axes[0].set_title(f"EUV Airy Disk PSF — NA={na}, λ={wavelength_nm} nm")
    axes[0].set_xlabel("x (nm)")
    axes[0].set_ylabel("y (nm)")
    plt.colorbar(im, ax=axes[0])

    # 1D cross-section
    center = len(x) // 2
    axes[1].plot(x, psf[center, :], "b-", linewidth=2)
    axes[1].set_xlabel("x (nm)")
    axes[1].set_ylabel("Normalized intensity")
    axes[1].set_title("PSF cross-section (y=0)")
    rayleigh_r = 0.61 * wavelength_nm / na
    axes[1].axvline(rayleigh_r, color="r", linestyle="--",
                    label=f"Rayleigh r = {rayleigh_r:.1f} nm")
    axes[1].axvline(-rayleigh_r, color="r", linestyle="--")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(x[0], x[-1])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print_performance_summary(NA, WAVELENGTH_NM, wfe_rms_nm=0.96)
    print()

    # Strehl vs WFE
    print("Strehl ratio vs wavefront RMS error:")
    print(f"{'WFE (nm)':>10}  {'WFE (λ)':>10}  {'Strehl':>10}")
    print("-" * 35)
    for wfe in [0.20, 0.40, 0.60, 0.80, 0.96, 1.20, 1.50]:
        s = strehl_from_wavefront_rms(wfe, WAVELENGTH_NM)
        print(f"{wfe:>10.2f}  {wfe/WAVELENGTH_NM:>10.3f}  {s:>10.4f}")

    print()
    print(f"Rayleigh resolution: {resolution_half_pitch(0.61, NA, WAVELENGTH_NM):.1f} nm HP")
    print(f"PSM/OPC resolution:  {resolution_half_pitch(0.32, NA, WAVELENGTH_NM):.1f} nm HP")
    print(f"Depth of focus:      ±{depth_of_focus(0.5, NA, WAVELENGTH_NM):.0f} nm")

    # Optional plots
    try:
        plot_mtf(NA, WAVELENGTH_NM)
        plot_psf(NA, WAVELENGTH_NM)
    except Exception:
        pass  # Plotting may fail in headless environments
