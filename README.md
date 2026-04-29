# OpenMC Hexagonal Fuel Assembly Model

## 📌 Overview
This project presents a **hexagonal fuel assembly model** developed using OpenMC. It demonstrates the implementation of material definitions, pin-cell modeling, and a multi-ring hexagonal lattice configuration for reactor simulation.

The repository is designed as part of a **technical documentation portfolio**, focusing on clarity, structure, and reproducibility of simulation workflows.

---

## 🖼️ Geometry Visualization

![Hexagonal Fuel Assembly](hex_fuel_assembly.png)

**Figure:** 2D visualization of the hexagonal fuel assembly generated using OpenMC.  
- Colors represent different materials (fuel, moderator, heat pipe)  
- Hexagonal symmetry confirms correct lattice construction  
- Used for validation of geometry setup  

---

## 🧠 Model Description

### Materials
The model includes three primary materials:
- **Fuel** – Uranium-based material for neutron production  
- **Heat Pipe** – Sodium-based thermal transport medium  
- **Moderator** – Water (H₂O) for neutron moderation  

---

### Geometry & Lattice

- Pin-cell based structure  
- Cylindrical regions for fuel and heat pipes  
- Axially bounded geometry using Z-planes  
- **3-ring hexagonal lattice configuration**  

Ring structure:
- Ring 0 (center): 1 pin  
- Ring 1: 6 pins  
- Ring 2: 12 pins  

Total: **19 lattice positions**

The lattice is implemented using OpenMC’s `HexLattice`, which requires:
- center
- pitch
- universes
- outer region  

Correct **outer-to-inner ordering** is critical for proper lattice definition.

---
