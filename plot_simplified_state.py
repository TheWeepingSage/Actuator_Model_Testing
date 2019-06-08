import numpy as np
import matplotlib.pyplot as plt

array_tc = np.loadtxt("simplified_actuator_tc_data_2.csv", delimiter=",")
array_minstep = np.loadtxt("simplified_actuator_minstep_data_2.csv", delimiter=",")
array_true = np.loadtxt("simplified_actuator_true_data_4.csv", delimiter=",")
time = np.linspace(0, 4, 4001, endpoint=True)

plt.plot(array_tc[:, 0], array_tc[:, 3], label="tc step w_3")
plt.plot(array_minstep[:, 0], array_minstep[:, 3], label="min step w_3")
plt.plot(time, array_true[:], label="true w_3")
plt.legend(loc="upper left")
plt.xlabel("Time(s)")
plt.ylabel("Angular Velocity")
plt.show()
