from ase.calculators.espresso import Espresso
from ase.db import connect
import re
from clease.tools import update_db
import os

#Setting up pseudopotentials and Hubbard Parameters
pseudo_dir = os.getcwd() + '/pseudos'
out_dir = os.getcwd() + '/out'

pseudopotentials = {'Mn': 'Mn.pbe-spn-kjpaw_psl.0.3.1.UPF',
                    'Ni': 'Ni.pbe-spn-kjpaw_psl.1.0.0.UPF',
                    'Sb': 'Sb.pbe-n-kjpaw_psl.1.0.0.UPF'}
#Setting up the database
db_name = "clease_MnNiSb.db"
db = connect(db_name)


# Use Monkhorst-Pack grid (3,3,3) for MnNi, 
# should change it to (11 ,11, 7) as generated from thr conversion Solveig code to CIF and then QUANTUM 
input_data = {
        'control': {
           'calculation': 'relax',
           'restart_mode': 'from_scratch',
           'pseudo_dir': pseudo_dir,
           'prefix': 'tutorial',        
            },
        'system': {
           'ecutwfc': 40.424222147,
           'ecutrho': 202.1211107,
           'occupations': 'smearing',
           'degauss': 0.0146997171,
           'lda_plus_u' : '.FALSE.',
          }, 
        'electrons': {
             'electron_maxstep': 200 	
          },
        }
calc = Espresso(pseudopotentials = pseudopotentials,
                input_data = input_data,
                kpts=(3,3,3))

cwd = os.getcwd()
#Connecting to the relevant database: this will the database which is gonna be modified by ase as well
#this will be the database that we will modify ourselves
db_name = "clease_MnNiSb.db"
db = connect(db_name)

"""Function that extracts the energy from the espresso.pwo file
 in case the get_potential_energy() method from ASE fails"""
def get_energies(filename):
    energies = []
    with open(filename,"r") as file:
        for line in file:
            pattern="!"
            if re.search(pattern, line):
                energies.append(re.findall(r'-?\d+', line))
        # Get the last calculated energy value before the calculation converges
        a = energies[-1][0]
        b = energies[-1][1]
        d = float(f'{a}.{b}') 
        #Important: we need to convert back from Rydberg to eV
        d = 13.60569193*d
        print("The final energies is ", d)
        return d
        
"""Updates the energy column for the given Atoms object given the id of the Atoms row (first column)"""
def update_energy(energy, id):
    with db.managed_connection() as con:
            cur = con.cursor()
            cur.execute(
                'UPDATE systems SET energy=? WHERE id=?',
                (energy, id))
            
"""Deletes from the database the configuration for which DFT calculations did not converge in 100 iterations"""
def handle_non_convergence(id):
    with db.managed_connection() as con:
            cur = con.cursor()
            cur.execute(
                'DELETE FROM systems WHERE id=?',
                (id,))

"""Updates the energy column for the given Atoms object given initial and final struct id once DFT is done"""
def update_converged_configs(initial_id, final_id):
    # get the id of the final structure whose calculation converged
    with db.managed_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT energy FROM systems WHERE id = ? AND energy IS NOT NULL", (initial_id,))
            # Fetch the result
            result = cur.fetchone()
            if result != None: 
                energy = result[0]
                cur.execute('UPDATE systems SET energy = (SELECT energy FROM systems WHERE id =? AND energy IS NOT NULL) WHERE id = ?', (initial_id, final_id))
                cur.execute("UPDATE systems SET energy = NULL WHERE id = ?", (initial_id,))


for row in db.select(converged=False):
    db.update(row.id, queued=True)
    print("We are analzying the following configuration")
    print(row.id, row.name)
    atoms = row.toatoms()
    atoms.calc = calc
    directory = 'espresso_{}'.format(row.id)
    parent_dir = cwd
    outputfile_path = os.path.join(parent_dir, directory)
    #if the first test fails, this try/except ensures that the calculations do not interfere with each other
    try:
        if not os.path.exists(outputfile_path):
            os.mkdir(outputfile_path)   
        # this was here just for testing purposes         
        #shutil.copy("espresso.pwo",path)
    except OSError as error:
        print(error)
        continue
    os.chdir(outputfile_path)
    try: 
         # For some reason, this method from ASE
        # will sometimes fail so we will get the energies computed by QE manually by reading the output file
        atoms.get_potential_energy()
    except:
        # For some reason, it will fail so we will just get the energy value manually from the created espresso,pwo file
        try:
            energy = get_energies("espresso.pwo")
            print("These are the energies")
            print(energy)
            update_energy(energy, row.id)
        # we need to handle the case where the DFT calculations do not converge: discard the configuration and delete
        # it from the database
        except: 
            #handle_non_convergence(row.id)
            continue
    os.chdir(cwd)
    update_db(uid_initial=row.id, final_struct=atoms, db_name=db_name)
    print("We have updated the database for the following row")
    print(row.id)


# Reset working directory to the default

# Reset working directory to the default one: uncomment when running script locally
os.chdir(cwd)

