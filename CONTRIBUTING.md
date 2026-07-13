# Contributing to OpenEUV

Thank you for your interest in contributing to OpenEUV! This project aims to build a comprehensive open-source reference for EUV lithography systems. Contributions from experts in optics, plasma physics, mechanical engineering, vacuum technology, control systems, and software are all welcome.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Contribution Areas](#contribution-areas)
4. [Pull Request Process](#pull-request-process)
5. [Documentation Style](#documentation-style)
6. [Simulation Code Standards](#simulation-code-standards)

---

## Code of Conduct

- Be respectful and constructive in all interactions.
- Back claims with references to published literature or first-principles calculations where possible.
- Acknowledge uncertainty — EUV lithography involves many proprietary details; distinguish between public knowledge and speculation.

---

## How to Contribute

1. **Fork** the repository on GitHub.
2. **Create a branch** from `main`: `git checkout -b feature/your-topic`.
3. **Make your changes** following the guidelines below.
4. **Test** any simulation code before submitting.
5. **Open a Pull Request** with a clear description of your changes.

---

## Contribution Areas

### Documentation (`docs/`)
- Correct technical errors or outdated information.
- Add missing design details, equations, or references.
- Translate content if helpful (though English is the primary language).

### Simulation (`software/simulation/`, `simulations/`)
- Improve optical models (ray-trace accuracy, aberration decomposition).
- Add plasma physics models for Sn LPP emission.
- Add stage servo control simulations.
- All simulation code must include a docstring and at least one usage example.

### Hardware Designs (`hardware/`)
- CAD drawings (FreeCAD `.FCStd` or STEP files preferred).
- Circuit schematics (KiCad preferred).
- Annotated photographs or measurement results from prototype subsystems.

### Bill of Materials (`bom/`)
- Updated vendor information, current pricing.
- Alternative component suggestions (especially open-source or lower-cost).

---

## Pull Request Process

1. Ensure your PR title summarizes the change (e.g., "Add collector mirror thermal model").
2. Reference any relevant issues (`Closes #XX`).
3. For simulation code, include a brief description of verification performed.
4. For documentation, cite your sources in the References section.
5. A maintainer will review and may request changes before merging.

---

## Documentation Style

- Write in clear, technical English.
- Use SI units throughout.
- Use Markdown tables for parameters and specifications.
- Use code blocks (` ``` `) for equations expressed as pseudocode, and LaTeX-style notation inline (`$equation$`) where rendering is supported.
- Keep section headings consistent with existing documents.

---

## Simulation Code Standards

- **Language**: Python 3.10+.
- **Dependencies**: List all dependencies in `software/simulation/requirements.txt`.
- **Style**: Follow PEP 8. Use type hints where practical.
- **Docstrings**: NumPy-style docstrings for all public functions.
- **Units**: Use SI units internally; document any conversions.
- **Testing**: Add a `__main__` block with a simple self-test or example.

Example function signature:
```python
def collector_efficiency(na: float, reflectance: float, n_bounces: int = 1) -> float:
    """
    Compute EUV collection efficiency for an ellipsoidal collector mirror.

    Parameters
    ----------
    na : float
        Numerical aperture of the collector (dimensionless).
    reflectance : float
        Peak EUV reflectance of the multilayer coating (0–1).
    n_bounces : int, optional
        Number of mirror reflections, by default 1.

    Returns
    -------
    float
        Fraction of 2π sr solid angle collected × reflectance^n_bounces.
    """
    solid_angle_fraction = (1 - np.sqrt(1 - na**2))  # fraction of hemisphere
    return solid_angle_fraction * (reflectance ** n_bounces)
```
