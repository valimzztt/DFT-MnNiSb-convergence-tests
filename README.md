# DFT_MnNiSb

Repository that collect Density Functional Theory (DFT) calculation and convergence tests for the intermetallic MnNiSb

In density functional theory (DFT) calculations, convergence tests of ENCUT and KPOINTS are crucial for obtaining accurate results. However, these tests are often neglected during the modeling phase since they require the submission of many short-time jobs, which requires extensive expertise in scripting, and command-line execution to handle the I/O files, which might be an issue for new users. We address this drawback by using workflow tools to manage the DFT calculations, which automate the process of performing convergence tests and ensure that the calculations are performed correctly. This can help to improve the accuracy and reliability of DFT results and prevent errors or inaccuracies from creeping into published research.

In this workflow, we utilize the powerful features of the SimStack framework to perform density functional theory (DFT) calculations for graphite with van der Waals correction applied to the AB stacking structure. By combining the **WaNos**: Graphire, Mult-It, DFT-VASP, QE-DFT, and DB-Generator, we can easily set up the graphite lattice parameters and choose the appropriate DFT methods using VASP or Quantum Espresso code.

The raw data from the DFT calculation is automatically parsed and stored in a human-readable, lightweight database in `.yml` format, which can be accessed from GitHub Repos using Google Colab. With the help of libraries like matplotlib, seaborn, and others, users can quickly search and filter the data based on specific criteria, allowing them to identify trends and patterns in complex systems. Overall, the SimStack framework makes it easy for users to gain valuable insights into the properties of graphite.

### In this workflow, we will be able to

```
1. SetSetting up floats, and integers or read the files' names from a given `.tar` (Mult-It).
2. Building the graphite structure by toggling the lattice parameters (Graphite).
3. Run the DFT calculations using QE or VASP code, accounting for the proper corrections (DFT-VASP or DFT-QE).
4. Generating a lightweight, human-readable database in `.yml` format for all **WaNos** of a 
  given workflow. 
```

## 1. Python Setup

To get this workflow up running on your available computational resources, make sure to have the below libraries installed on Python 3.6 or newer.

```
1. Atomic Simulation Environment (ASE).
2. Python Materials Genomics (Pymatgen).
3. Numpy, os, sys, re, yaml, subprocess.
4. json, csv, shutil, tarfile. 
```

## 2. Mult-Mol Inputs

- Range of the variable position.
- Number of points in the present in the range.
- Beginning of the Molecule name, which should appear in all molecules.
- Directory with the zip file of the molecules.

## 3. Mult-Mol Output

- It should pass all the information to the next WaNo inside the ForEach loop through the `Mult_Mol.iter.*` command on the top of the loop, as Fig 1 shows in step 2.

## 4. Surface Inputs

- Aux_var should be set as `${ForEach_iterator_ITER}` from import workflow variable.
- Mol_name should be set as `Mult_Mol.Molecule_name` from import workflow variable.
- Defining bulk unit cell types, element, and lattice constant.
- Defining slab size, vacuum size, Miller index of the surface, and as an option, set a supercell.
- Check the box when you want to adsorb a molecule on the surface previously defined.
- Setting the molecule distance over the surface and molecule-molecule image distance.

## 5. Surface Output

- POSCAR and Input_data.yml files, which should be passed to DFT-VASP **WaNo**.

## 6. DFT-VASP Inputs

- **INCAR tab**: as an option, we can set all INCAR flags available within VASP. However, we expose only a few of them, which are essential for the problem. See the GUI of this WaNo. A brief description of each flag pops up when we rover the mouse over the inputs.
- **KPOINTS tab**: Here the user can define two types of KPOINTS, `Kpoints_length` and `Kpoints_Monkhorst`.
- **Analysis tab**: Aimed to compute Bader charge analysis and DOS.
- **Files_Run tab**: Mandatory loads the POSCAR file, and as an option can load INCAR, POTCAR, KPOINTS, and KORINGA files. The KORINGA file can be any file. In the case of this problem, it loads the Input_data.yml file.

## 7. DFT-VASP Output

- OUTCAR file.

## 8. Table-Generator Inputs

- Search_in_File: Should be set as OUTCAR and import the OUTCAR file using `ForEach/*/DFT_VASP/outputs/OUTCAR` command.
- Delete_Files: check the box option.
- Search_Parameters: Set the variables `z_0`, `File_number`, and `energy`.  

## 9. Table-Generator Output

- Table-var file in CSV format containing the variables defined in the Search_Parameters field.

## Acknowledgements

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 957189. The project is part of BATTERY 2030+, the large-scale European research initiative for inventing the sustainable batteries of the future.

## License & copyright

  Developer: Celso Ricardo C. Rêgo,
  Multiscale Materials Modelling and Virtual Design,
  Institute of Nanotechnology, Karlsruhe Institute of Technology
  <https://www.int.kit.edu/wenzel.php>

Licensed under the [KIT License](LICENSE).
