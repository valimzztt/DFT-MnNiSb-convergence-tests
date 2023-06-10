#!/bin/sh
module purge
module add impi sci/dft sci/qe_7.2
export MKL_NUM_THREADS=1
export ASE_ESPRESSO_COMMAND="mpirun /home/sci/opt/qe-7.2_impi/bin/pw.x -np 4 < PREFIX.pwi > PREFIX.pwo"
NAME="scfkpoint"
declare -A energy_dict  # Declare an associative array for storing energies

for KPOINT in 4 5 6 7 8
do
echo $KPOINT
cat > ${NAME}_${KPOINT}.in << EOF
&CONTROL
  calculation = 'scf'
  etot_conv_thr =   1.6000000000d-04
  forc_conv_thr =   1.0000000000d-04
  outdir = './out/'
  prefix = 'aiida'
  pseudo_dir = './pseudos/'
  tprnfor = .true.
  tstress = .true.
  verbosity = 'high'
/
&SYSTEM
  degauss =   1.4699723600d-02
  ecutrho =   7.8000000000d+02
  ecutwfc =   6.5000000000d+01
  ibrav = 0
  nat = 16
  nosym = .false.
  nspin = 2
  ntyp = 3
  occupations = 'smearing'
  smearing = 'cold'
  starting_magnetization(1) =   3.3333333333d-01
  starting_magnetization(2) =   2.7777777778d-01
  starting_magnetization(3) =   1.0000000000d-01
/
&ELECTRONS
  conv_thr =   3.2000000000d-09
  electron_maxstep = 80
  mixing_beta =   4.0000000000d-01
/
ATOMIC_SPECIES
Mn 54.938044 Mn.pbe-spn-kjpaw_psl.0.3.1.UPF
Ni 58.6934 Ni.pbe-spn-kjpaw_psl.1.0.0.UPF
Sb 121.76 Sb.pbe-n-kjpaw_psl.1.0.0.UPF
ATOMIC_POSITIONS crystal
Mn           0.0000000000       0.0000000000       0.0000000000 
Mn           0.0000000000       0.5000000000       0.5000000000 
Mn           0.5000000000       0.0000000000       0.5000000000 
Mn           0.5000000000       0.5000000000       0.0000000000 
Ni           0.2500000000       0.7500000000       0.7500000000 
Ni           0.2500000000       0.2500000000       0.7500000000 
Ni           0.2500000000       0.2500000000       0.2500000000 
Ni           0.2500000000       0.7500000000       0.2500000000 
Ni           0.7500000000       0.7500000000       0.2500000000 
Ni           0.7500000000       0.2500000000       0.2500000000 
Ni           0.7500000000       0.2500000000       0.7500000000 
Ni           0.7500000000       0.7500000000       0.7500000000 
Sb           0.0000000000       0.0000000000       0.5000000000 
Sb           0.0000000000       0.5000000000       0.0000000000 
Sb           0.5000000000       0.0000000000       0.0000000000 
Sb           0.5000000000       0.5000000000       0.5000000000 
K_POINTS automatic
$KPOINT $KPOINT $KPOINT 0 0 0
CELL_PARAMETERS angstrom
      6.0531980000       0.0000000000       0.0000000000
      0.0000000000       6.0531980000       0.0000000000
      0.0000000000       0.0000000000       6.0531980000
EOF

pw.x < ${NAME}_${KPOINT}.in > ${NAME}_${KPOINT}.out
echo ${NAME}_${KPOINT}
grep ! ${NAME}_${KPOINT}.out
energy=$(grep "!" "${NAME}_${KPOINT}.out" | awk '{print $5}')  # Extract the energy value using awk
energy_dict["${KPOINT}"]=$energy  # Store energy in the dictionary with cutoff value as key
done
# Print the dictionary
for key in "${!energy_dict[@]}"; do
    echo "KPOINT: $key, Energy: ${energy_dict[$key]}"
    # Save energies in text file with corresponding cutoff
    echo "$key ${energy_dict[$key]}" >> "energies.txt"
done
