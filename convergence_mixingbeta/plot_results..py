import matplotlib.pyplot as plt
import os 
cwd = os.getcwd()
dir_conv = 'convergence_mixingbeta'
filename = os.path.join(dir_conv, 'energies.txt')
data = {}

# Read the text file
with open(filename, 'r') as file:
    lines = file.readlines()

# Process each line and extract mixing beta and energy
for line in lines:
    cutoff, energy = line.split(', ')
    cutoff = int(cutoff.split(': ')[1])/100
    energy = float(energy.split(': ')[1])
    data[cutoff] = energy

# Extract mixing beta and energies
mixing_beta = list(data.keys())
energies = list(data.values())

# Plotting
plt.scatter(mixing_beta, energies)
plt.xlabel("Mixing Beta")
plt.ylabel("Energy")
plt.title("Energy vs Mixing Beta")
plt.grid(True)
plt.show()
