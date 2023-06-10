#setup directory
import os

#define concentration range of all elements
from clease.settings import Concentration
conc = Concentration(basis_elements=[['Mn', 'Ni'], ['Sb']])
conc.set_conc_ranges(ranges=[[(0,1),(0,1)], [(1,1)]])


#define crystal structure
from clease.settings import CECrystal
settings = CECrystal(concentration=conc, 
    spacegroup=164, 
    basis=[(0.00000, 0.00000, 0.00000), (0.33333333, 0.66666667, 0.25)], 
    cell=[4.00, 4.00,   5.46, 90, 90, 120],  
    supercell_factor=8, 
    db_name="clease_MnNiSb.db", 
    basis_func_type='binary_linear',
   max_cluster_dia=(7,7,7))

#generate first round of structures
from clease import NewStructures
ns = NewStructures(settings, generation_number=0, struct_per_gen=20)
ns.generate_initial_pool()

from ase.db import connect
db = connect('clease_MnNiSb.db')
del  db[db.get(id='1').id]