import json
import matplotlib.pyplot as plt
import os 
cwd = os.getcwd()
dir_conv = 'convergence_kpts'
filename = os.path.join(dir_conv, 'results.json')
# Read JSON file and convert to dictionary
with open(filename, 'r') as file:
    data = json.load(file)

# Extract kpoints and energies
kpoints = []
energies = []
for key, value in data.items():
    kpoints.append(int(key))
    energy = float(value.split(',')[0].strip()[1:])
    energies.append(energy)

# Plotting
plt.plot(kpoints, energies, marker='o')
plt.xlabel("KPOINTS")
plt.ylabel("Energy")
plt.title("Energy vs KPOINTS")
plt.grid(True)
plt.show()

