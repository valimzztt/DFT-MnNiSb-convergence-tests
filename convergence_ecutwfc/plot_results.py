dictionary = {10: -1240.43441030, 15: -1257.70183652, 20:-1263.95322051, 25:-1266.76706738, 30:-1267.31241235, 35:-1267.49654679,
 40:-1267.51174110, 45:-1267.51400413, 50:-1267.51518346, 55: -1267.51758375, 60:-1267.51993922, 65:-1267.52106661, 70:-1267.52148418, 75:-1267.52151902}

# import required module
import os
cwd = os.getcwd()

import matplotlib.pyplot as plt
x = list(dictionary.keys())
y = list(dictionary.values())

plt.plot(x, y, marker='o')
plt.xlabel('Kinetic energy cutoff (Ry) for wavefunctions (ecutwfc)')
plt.ylabel('Final Energies (R)')
plt.title('Plot of Final Energies (Ry) versus ecutwfc (Ry) in QE')
plt.grid(True)
plt.show()

