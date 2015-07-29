import openmc


###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 202
inactive = 200 
particles = 10000


###############################################################################
#                 Exporting to OpenMC materials.xml File
###############################################################################

# Instantiate some Nuclides
h1 = openmc.Nuclide('H-1')
o16 = openmc.Nuclide('O-16')
u235 = openmc.Nuclide('U-235')

# Instantiate some Materials and register the appropriate Nuclides
homog = openmc.Material(material_id=1, name='homogeneous')
homog.set_density('g/cc', 5.0)
homog.add_nuclide(h1, 2.)
homog.add_nuclide(o16, 1.)
homog.add_nuclide(u235, 0.001)
homog.add_s_alpha_beta('HH2O', '71t')

# Instantiate a MaterialsFile, register all Materials, and export to XML
materials_file = openmc.MaterialsFile()
materials_file.default_xs = '71c'
materials_file.add_materials([homog])
materials_file.export_to_xml()


###############################################################################
#                 Exporting to OpenMC geometry.xml File
###############################################################################

# Instantiate surfaces
surf1 = openmc.XPlane(surface_id=1, x0=-200.0, name='surf 1', boundary_type='reflective')
surf2 = openmc.XPlane(surface_id=2, x0=+200.0, name='surf 2', boundary_type='reflective')
surf3 = openmc.YPlane(surface_id=3, y0=-200.0, name='surf 3', boundary_type='reflective')
surf4 = openmc.YPlane(surface_id=4, y0=+200.0, name='surf 4', boundary_type='reflective')
surf5 = openmc.ZPlane(surface_id=5, z0=-2.0, name='surf 5', boundary_type='reflective')
surf6 = openmc.ZPlane(surface_id=6, z0=+2.0, name='surf 6', boundary_type='reflective')

# Instantiate Cells
cell1 = openmc.Cell(cell_id=1, name='cell 1')

# Register Surfaces with Cells
cell1.add_surface(surface=surf1, halfspace=+1)
cell1.add_surface(surface=surf2, halfspace=-1)
cell1.add_surface(surface=surf3, halfspace=+1)
cell1.add_surface(surface=surf4, halfspace=-1)
cell1.add_surface(surface=surf5, halfspace=+1)
cell1.add_surface(surface=surf6, halfspace=-1)

# Register Materials with Cells
cell1.fill = homog

# Instantiate Universes
root = openmc.Universe(universe_id=0, name='root universe')

# Register Cells with Universes
root.add_cells([cell1])

# Instantiate a Geometry and register the root Universe
geometry = openmc.Geometry()
geometry.root_universe = root

# Instantiate a GeometryFile, register Geometry, and export to XML
geometry_file = openmc.GeometryFile()
geometry_file.geometry = geometry
geometry_file.export_to_xml()


###############################################################################
#                   Exporting to OpenMC settings.xml File
###############################################################################

# Instantiate a SettingsFile, set all runtime parameters, and export to XML
settings_file = openmc.SettingsFile()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles
settings_file.set_source_space('box', [-200.0, -200.0, -2.0, 200.0, 200.0, 2.0])
settings_file.statepoint_interval = 1
settings_file.entropy_dimension = [200, 200, 2]
settings_file.entropy_lower_left = [-200.0, -200.0, -2.0]
settings_file.entropy_upper_right = [200.0, 200.0, 2.0]
settings_file.export_to_xml()
