import json
import matplotlib.pyplot as plt
import os 
cwd = os.getcwd()
dir_conv = 'convergence_ecutrho'
filename = os.path.join(dir_conv, 'energies.txt')
# Read the text file
with open(filename , 'r') as file:
    lines = file.readlines()

# Create a dictionary to store the energies
energies = {}

# Process each line and populate the dictionary
for line in lines:
    key, value = line.strip().split(' ')
    energies[int(key)] = float(value)

# Save energies as a JSON file
with open('energies.json', 'w') as file:
    json.dump(energies, file)

# Plot the energies
plt.plot(list(energies.keys()), list(energies.values()))
plt.xlabel('Multiplication factor for Kinetic energy cutoff (Ry) of wavefunctions (ecutrho)')
plt.ylabel('Final Energies (R)')
plt.title('Plot of Final Energies (Ry) versus ecutwfc (Ry) in QE')
plt.show()

