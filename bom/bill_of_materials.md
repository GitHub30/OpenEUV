# Bill of Materials (BOM)

> **Note**: All costs are rough estimates in USD for research-grade prototype quantities (1 unit). Production quantities would reduce costs significantly. Prices are approximate as of 2024 and subject to change. Many components require custom fabrication and vendor negotiation.

---

## 1. EUV Light Source

### 1.1 CO₂ Drive Laser

| Item | Specification | Quantity | Estimated Unit Cost | Vendor (Examples) |
|---|---|---|---|---|
| CO₂ laser oscillator | 10.6 µm, CW, 100 W | 1 | $50,000 | Coherent, Synrad |
| CO₂ pre-amplifier modules | 10.6 µm, pulsed, 1 kW each | 3 | $150,000 | TRUMPF, GSI Group |
| CO₂ main amplifier | 10.6 µm, pulsed, ≥10 kW | 1 | $1,500,000 | TRUMPF, Coherent |
| Acousto-optic modulator (AOM) | 10.6 µm, 50 kHz rep rate | 1 | $20,000 | II-VI, Intraaction |
| Off-axis parabolic mirror (OAP) | Gold-coated Cu, f=300 mm | 2 | $8,000 | Janos, Edmund Optics |
| ZnSe focusing lens | AR-coated, 10.6 µm, f=300 mm | 2 | $5,000 | II-VI, Crystran |
| Gold-coated flat mirrors | Cu substrate, 100 mm dia. | 10 | $2,000 | Janos, Ophir |
| Beam transport tube | 316 SS, interlocked | 1 set | $30,000 | Custom |
| Beam dump (main) | Water-cooled W/Cu | 2 | $15,000 | Kentek, Coherent |
| Power meter / calorimeter | 10.6 µm, 0–50 kW | 2 | $10,000 | Ophir, Coherent |
| Laser power supply | 480V 3-phase, 100 kW | 1 | $50,000 | Custom / AMETEK |
| **Subtotal** | | | **~$1,900,000** | |

### 1.2 Tin Droplet Generator

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Droplet generator head | Piezo, W orifice, 17 µm | 1 | $80,000 | Microfab, Custom |
| Tin feedstock | 99.9999% Sn, 1 kg ingots | 10 | $500 | Alfa Aesar |
| Tin reservoir | Heated, 1 L, W-coated | 1 | $15,000 | Custom |
| Piezo driver electronics | 50 kHz, ±100 V | 1 | $10,000 | PI Ceramic, Thorlabs |
| Droplet position sensor | Stroboscopic laser | 1 | $25,000 | Custom |
| Droplet catcher | Water-cooled W cone | 1 | $20,000 | Custom |
| Heater controller | 4-zone, ±0.1°C | 1 | $5,000 | Watlow, Omega |
| **Subtotal** | | | **~$160,000** | |

### 1.3 Source Chamber

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Source chamber body | 316L SS, 500 mm dia. | 1 | $40,000 | Custom fab |
| CF flanges & fittings | Various sizes | 1 set | $8,000 | MDC Vacuum, Kurt Lesker |
| ZnSe viewport | 10.6 µm, CF40 | 2 | $3,000 | II-VI |
| Turbomolecular pump | 2000 L/s, maglev | 1 | $25,000 | Pfeiffer, Edwards |
| Dry scroll roughing pump | 12 m³/h | 1 | $8,000 | Leybold, Edwards |
| Mass flow controller (H₂) | 0–200 sccm | 1 | $1,500 | MKS, Alicat |
| Capacitance manometer | 0–100 Pa | 2 | $2,000 | MKS Baratron |
| Bake-out heater tape | 150°C rated | 1 set | $2,000 | Omega |
| Ion gauge | BAG-type | 2 | $1,500 | Granville-Phillips |
| H₂ gas detector | 0–4% LEL | 2 | $1,000 | MSA, RKI |
| **Subtotal** | | | **~$100,000** | |

---

## 2. Collector Mirror

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Zerodur® blank | 700 mm dia., Grade 0 | 1 | $50,000 | Schott |
| CNC grinding / polishing | Ellipsoidal figure, 0.1 nm rms | 1 | $300,000 | Zygo, Tinsley |
| Ion beam figuring (IBF) | Final figure correction | 1 | $100,000 | Opticus, Zeeko |
| Mo/Si multilayer coating (IBD) | Graded, 50 bilayers | 1 | $100,000 | Lawrence Livermore, NIST |
| EUV reflectance metrology | Synchrotron beamline time | 5 visits | $20,000 | ALS, ESRF |
| Stitching interferometry | Asphere verification | 1 | $20,000 | Zygo service |
| Invar mirror mount | Kinematic, 5-DOF adjust | 1 | $30,000 | Custom |
| Cooling manifold | UPW-cooled, bonded | 1 | $15,000 | Custom |
| **Subtotal** | | | **~$635,000** | |

---

## 3. Illumination System

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| FFM substrate + facets | 122 Mo/Si facets, 7.4×1.4 mm | 1 set | $200,000 | Custom |
| FFM piezo actuators | 6-DOF per cluster, 100 facets | 1 set | $50,000 | PI, Physik Instrumente |
| PFM substrate + facets | 122 Mo/Si facets, 6 mm dia. | 1 set | $150,000 | Custom |
| Transfer mirrors | Ru-coated, grazing, 4× | 4 | $20,000 | Custom |
| ILS chamber | 316L SS, 1000×500×500 mm | 1 | $30,000 | Custom fab |
| Vacuum equipment | TMP, gauges, valves | 1 set | $30,000 | Pfeiffer, MDC |
| Spectral purity filter | Grazing Si mirror | 1 | $15,000 | Custom |
| **Subtotal** | | | **~$495,000** | |

---

## 4. Projection Optics Box (POB)

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Mirror blanks (M1–M6) | ULE®, various sizes | 6 | $30,000 | Corning |
| Mirror polishing (M1–M6) | Aspheric, IBF, 0.1 nm rms | 6 | $500,000 | Zygo, Asahi, Tinsley |
| Mo/Si graded coating | Each mirror | 6 | $60,000 | Specialized fab |
| At-wavelength wavefront sensor | EUV Hartmann | 1 | $200,000 | Custom / Zemax |
| CGH test plates | For asphere null testing | 6 | $30,000 | Diffraction International |
| POB housing (CFRP/Invar) | 1.8 m × 0.8 m | 1 | $150,000 | Custom |
| Mirror mounts with piezos | 6-DOF, nm precision | 6 | $30,000 | PI, Attocube |
| Thermal control system | 22°C ± 1 mK | 1 | $50,000 | Custom |
| POB vacuum system | TMP, ion pump, cryo panel | 1 set | $80,000 | Pfeiffer, SAES |
| **Subtotal** | | | **~$1,220,000** | |

> **Note**: High-quality 6-mirror EUV optics for a production system can cost $5M–$20M+. This estimate assumes research-grade optics with relaxed specifications.

---

## 5. Reticle Stage

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Linear motors (ironless, X-Y) | 2000 N peak, ±150 mm | 2 | $30,000 | Aerotech, LinMot |
| Air bearing guideways | X-Y, granite base | 1 set | $80,000 | Dover Motion, New Way |
| Lorentz actuators (6-DOF fine) | 100 N, ±3 mm | 6 | $5,000 | Custom |
| Electrostatic chuck | 152 mm, Zerodur, bipolar | 1 | $40,000 | Creative Technology, Custom |
| Laser interferometer (reticle) | 3-axis, HeNe, 0.1 nm | 1 set | $50,000 | Zygo, Renishaw |
| Reference mirrors (Zerodur) | λ/20 flat | 2 | $15,000 | Zygo |
| Servo amplifiers | 4-quadrant, 50 kHz | 8 | $3,000 | ACS, Aerotech |
| Metrology frame | Zerodur structure | 1 | $40,000 | Custom |
| Balance mass mechanism | Counter-moving, cable drive | 1 | $20,000 | Custom |
| **Subtotal** | | | **~$340,000** | |

---

## 6. Wafer Stage

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Planar motor stator | 400×400 mm coil array | 1 | $80,000 | Akribis, Tecnotion |
| Planar motor mover | Magnet array, SiC plate | 1 | $40,000 | Akribis, Custom |
| Lorentz actuators (fine, 6-DOF) | ±75 N, ±3 mm | 6 | $5,000 | Custom |
| Electrostatic chuck (300 mm) | AlN, thermal control | 1 | $50,000 | Creative Technology, Entegris |
| Laser interferometer (wafer) | 3-axis, HeNe, 0.1 nm | 1 set | $50,000 | Zygo, Renishaw |
| Focus/leveling sensor | 9-point optical, 1 nm | 1 | $40,000 | Nikon, Custom |
| Reference mirrors (Zerodur) | λ/20 flat | 2 | $15,000 | Zygo |
| Servo amplifiers | 4-quadrant, 50 kHz | 8 | $3,000 | ACS, Aerotech |
| Granite base | Grade A, 1.5 m × 1.5 m | 1 | $30,000 | Microplan, Standridge |
| Wafer handling robot | Atmospheric, 300 mm | 1 | $40,000 | Brooks, Kawasaki |
| **Subtotal** | | | **~$390,000** | |

---

## 7. Vacuum System (overall)

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Turbomolecular pumps | Various, 500–2000 L/s | 8 | $15,000 | Pfeiffer, Edwards |
| Dry scroll pumps | 12–30 m³/h | 4 | $6,000 | Leybold, Busch |
| Ion pumps | 200–500 L/s | 3 | $8,000 | Gamma Vacuum, Varian |
| Cryogenic panels | LN₂-cooled | 4 | $10,000 | Heliogen, Custom |
| Vacuum valves (gate, butterfly) | CF flanges, interlocked | 30 | $2,000 | VAT, MDC |
| Residual gas analyzer (RGA) | 1–200 amu | 2 | $15,000 | MKS, Pfeiffer |
| Vacuum gauges (various) | IG, CM, Pirani | 20 | $1,000 | MKS, Pfeiffer |
| Loadlock chambers (2×) | 300 mm wafer + reticle | 2 | $30,000 | Custom |
| Piping, fittings, flanges | CF, VCR, ISO | 1 set | $30,000 | MDC, Kurt Lesker |
| **Subtotal** | | | **~$350,000** | |

---

## 8. Control System

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| FPGA controller (Zynq-7000) | Xilinx Zynq UltraScale+ | 4 | $5,000 | AMD/Xilinx, Enclustra |
| Real-time PC | Ubuntu RT, 8-core | 2 | $5,000 | Dell, Custom |
| Supervisory PC | Workstation-class | 1 | $5,000 | Dell, HP |
| ADC/DAC boards | 16-bit, ±10 V, 100 kHz | 8 | $2,000 | National Instruments, Measurement Computing |
| Motor drive amplifiers | Linear, 50 kHz BW | 20 | $2,000 | ACS, Aerotech |
| EtherCAT network | Switches, cables | 1 set | $5,000 | Beckhoff |
| UPS (uninterruptible power) | 10 kVA | 2 | $10,000 | APC, Eaton |
| Control cabinet | 19-inch rack, EMC shielded | 4 | $5,000 | Rittal |
| Cabling harness | Signal + power | 1 set | $20,000 | Custom |
| **Subtotal** | | | **~$115,000** | |

---

## 9. Metrology

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Zeeman HeNe laser | 632.8 nm, frequency-stabilized | 2 | $15,000 | Zygo, Agilent |
| Interferometer optics | Beam splitters, retro-reflectors | 2 sets | $20,000 | Zygo, Agilent |
| Zerodur metrology frame | Low CTE reference structure | 1 | $100,000 | Custom |
| Capacitance gauges (reticle) | 5 nm resolution | 8 | $3,000 | Lion Precision, Micro-Epsilon |
| Wavefront sensor (EUV Hartmann) | 13.5 nm, CCD-based | 1 | $150,000 | Custom / Zygo |
| EUV photodiode (power monitor) | Si PIN, 13.5 nm | 2 | $5,000 | International Radiation Detectors |
| **Subtotal** | | | **~$340,000** | |

---

## 10. Cleanroom and Facility

| Item | Specification | Quantity | Estimated Unit Cost | Vendor |
|---|---|---|---|---|
| Cleanroom construction | ISO Class 3, 100 m² | 1 | $2,000,000 | M+W, Exyte |
| Vibration isolation table | Active, 2 m × 3 m, VC-E | 1 | $200,000 | TMC, Newport |
| Seismic sensor + active isolation | 6-DOF, 0.1–100 Hz | 1 | $100,000 | Herzan, HWL |
| HVAC system | 22°C ± 0.1°C, ULPA | 1 | $300,000 | Custom |
| Chemical/gas distribution | N₂, CDA, H₂, UPW | 1 set | $100,000 | Custom |
| Electrical power | 480V 3-phase, 200 kVA | 1 | $100,000 | Custom |
| Fire suppression | FM-200 or Novec 1230 | 1 | $50,000 | Kidde |
| **Subtotal** | | | **~$2,850,000** | |

---

## 11. Grand Total Estimate

| Subsystem | Estimated Cost (USD) |
|---|---|
| CO₂ Drive Laser | $1,900,000 |
| Tin Droplet Generator + Source Chamber | $260,000 |
| Collector Mirror | $635,000 |
| Illumination System | $495,000 |
| Projection Optics Box | $1,220,000 |
| Reticle Stage | $340,000 |
| Wafer Stage | $390,000 |
| Vacuum System | $350,000 |
| Control System | $115,000 |
| Metrology | $340,000 |
| Cleanroom and Facility | $2,850,000 |
| **Contingency (20%)** | **$1,779,000** |
| **TOTAL** | **~$10,674,000** |

> **Disclaimer**: These are rough estimates for planning purposes only. Actual costs depend heavily on specifications, vendor selection, quantity, and market conditions. Professional cost estimation is required for any serious project planning. Production EUV scanners (ASML NXE:3600D) cost approximately $380 million each due to extreme precision and volumes of production-grade components.
