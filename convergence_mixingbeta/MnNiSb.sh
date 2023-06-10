#!/bin/sh
module purge
module add impi sci/dft sci/qe_7.2
export MKL_NUM_THREADS=1
export ASE_ESPRESSO_COMMAND="mpirun /home/sci/opt/qe-7.2_impi/bin/pw.x -np 4 < PREFIX.pwi > PREFIX.pwo"
NAME="mixingbeta"
declare -A energy_dict  # Declare an associative array for storing energies

for BETA in 2 3 4 5 6 7
do
echo $BETA
mixingbeta=$((BETA  / 10))
# Divide by 10 and store the result in a new variable
echo $mixingbeta
cat > ${NAME}_${BETA}.in << EOF
&CONTROL
  calculation = 'relax'
  etot_conv_thr =   4.0000000000d-05
  forc_conv_thr =   1.0000000000d-04
  outdir = './out/'
  prefix = 'MnNiSb'
  pseudo_dir = './pseudos/'
  tprnfor = .true.
  tstress = .true.
/
&SYSTEM
  degauss =   0.0146997171
  ecutrho =   202.1211107
  ecutwfc =   40.424222147
  ibrav = 0
  nat = 4
  nosym = .false.
  ntyp = 3
  occupations = 'smearing'
  starting_magnetization(1) =   3.3333333333d-01
  starting_magnetization(2) =   2.7777777778d-01
  starting_magnetization(3) =   1.0000000000d-01
/
&ELECTRONS
  conv_thr =   8.0000000000d-10
  electron_maxstep = 100
  mixing_beta =   $mixingbeta
/
&IONS
/
&CELL
/
ATOMIC_SPECIES
Mn 54.938044 Mn.pbe-spn-kjpaw_psl.0.3.1.UPF
Ni 58.6934 Ni.pbe-spn-kjpaw_psl.1.0.0.UPF
Sb 121.76 Sb.pbe-n-kjpaw_psl.1.0.0.UPF

ATOMIC_POSITIONS crystal
Mn           0.0000000000       0.0000000000       0.5000000000 
Ni           0.0000000000       0.0000000000       0.0000000000 
Sb           0.3333333300       0.6666666700       0.2343760000 
Sb           0.6666666700       0.3333333300       0.7656240000

K_POINTS automatic
11 11 11 0 0 0

CELL_PARAMETERS angstrom
      3.9953378200       0.0000000000       0.0000000000
     -1.9976689100       3.4600640488       0.0000000000
      0.0000000000       0.0000000000       5.4618040000
EOF

pw.x < ${NAME}_${BETA}.in > ${NAME}_${BETA}.out
echo ${NAME}_${BETA}
grep ! ${NAME}_${BETA}.out
energy=$(grep "!" "${NAME}_${BETA}.out" | awk '{print $5}')  # Extract the energy value using awk
energy_dict["${BETA}"]=$energy  # Store energy in the dictionary with cutoff value as key
done
# Print the dictionary
for key in "${!energy_dict[@]}"; do
    echo "BETA: $key, Energy: ${energy_dict[$key]}"
    # Save energies in text file with corresponding BETA mixing value
    echo "$key ${energy_dict[$key]}" >> "energies.txt"
done
