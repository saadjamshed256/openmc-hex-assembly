"""
OpenMC Hexagonal Fuel Assembly Model
------------------------------------

Description:
This script models a simple 3-ring hexagonal fuel assembly using OpenMC.
It demonstrates material definition, pin cell construction, and hexagonal
lattice implementation.

Author: Saad Jamshed
Project: OpenMC Documentation Portfolio

Requirements:
- Python 3.x
- OpenMC installed and configured

Run:
    python hex_assembly.py
"""

import openmc


# =============================================================================
# MATERIAL DEFINITIONS
# =============================================================================
def create_materials():
    """Define and export materials."""
    
    fuel = openmc.Material(name='Fuel')
    fuel.add_element('U', 1.0)
    fuel.set_density('g/cm3', 10.5)

    heat_pipe = openmc.Material(name='Heat Pipe')
    heat_pipe.add_element('Na', 1.0)
    heat_pipe.set_density('g/cm3', 0.97)

    moderator = openmc.Material(name='Moderator')
    moderator.add_element('H', 2)
    moderator.add_element('O', 1)
    moderator.set_density('g/cm3', 1.0)

    materials = openmc.Materials([fuel, heat_pipe, moderator])
    materials.export_to_xml()

    return fuel, heat_pipe, moderator


# =============================================================================
# PIN CELL CREATION
# =============================================================================
def create_pin_universes(fuel, heat_pipe, moderator):
    """Create pin cell universes for fuel and heat pipe."""

    fuel_radius = openmc.ZCylinder(r=0.4)
    fuel_cell = openmc.Cell(fill=fuel, region=-fuel_radius)
    fuel_universe = openmc.Universe(cells=[fuel_cell])

    hp_radius = openmc.ZCylinder(r=0.4)
    hp_cell = openmc.Cell(fill=heat_pipe, region=-hp_radius)
    hp_universe = openmc.Universe(cells=[hp_cell])

    moderator_cell = openmc.Cell(fill=moderator)
    moderator_universe = openmc.Universe(cells=[moderator_cell])

    return fuel_universe, hp_universe, moderator_universe


# =============================================================================
# HEXAGONAL LATTICE CONSTRUCTION
# =============================================================================
def create_hex_lattice(fuel_universe, moderator_universe):
    """
    Create a 3-ring hexagonal lattice.

    Ring structure:
    Ring 0 (center): 1
    Ring 1: 6
    Ring 2: 12
    """

    hex_lattice = openmc.HexLattice()
    hex_lattice.center = (0.0, 0.0)
    hex_lattice.pitch = (1.0,)

    # IMPORTANT: OpenMC expects OUTER → INNER ordering
    hex_lattice.universes = [
        [fuel_universe] * 12,  # Outer ring (Ring 2)
        [fuel_universe] * 6,   # Middle ring (Ring 1)
        [fuel_universe] * 1    # Center (Ring 0)
    ]

    hex_lattice.outer = moderator_universe

    return hex_lattice


# =============================================================================
# GEOMETRY SETUP
# =============================================================================
def create_geometry(hex_lattice):
    """Create and export geometry."""

    z_min = openmc.ZPlane(z0=-1.0)
    z_max = openmc.ZPlane(z0=1.0)

    lattice_cell = openmc.Cell(
        fill=hex_lattice,
        region=+z_min & -z_max
    )

    root_universe = openmc.Universe(cells=[lattice_cell])
    geometry = openmc.Geometry(root_universe)
    geometry.export_to_xml()


# =============================================================================
# PLOTTING
# =============================================================================
def create_plot():
    """Generate geometry plot for visualization."""

    plot = openmc.Plot()
    plot.filename = 'hex_fuel_assembly'
    plot.origin = (0.0, 0.0, 0.0)
    plot.width = (7.0, 7.0)
    plot.pixels = (800, 800)
    plot.color_by = 'material'
    plot.basis = 'xy'

    plots = openmc.Plots([plot])
    plots.export_to_xml()

    openmc.plot_geometry()


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """Main execution function."""

    fuel, heat_pipe, moderator = create_materials()

    fuel_universe, hp_universe, moderator_universe = create_pin_universes(
        fuel, heat_pipe, moderator
    )

    hex_lattice = create_hex_lattice(fuel_universe, moderator_universe)

    create_geometry(hex_lattice)

    create_plot()

    print("✔ OpenMC hexagonal lattice model generated successfully.")


if __name__ == "__main__":
    main()