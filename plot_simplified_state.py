import numpy as np
import matplotlib.pyplot as plt

array_tc = np.loadtxt("simplified_actuator_tc_data_2.csv", delimiter=",")
array_minstep = np.loadtxt("simplified_actuator_minstep_data_2.csv", delimiter=",")

plt.plot(array_tc[:, 0], array_tc[:, 3], label="tc step w_1")
plt.plot(array_minstep[:, 0], array_minstep[:, 3], label="min step w_1")
plt.legend()
plt.show()
