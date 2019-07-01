import numpy as np
import matplotlib.pyplot as plt

control_step = 2
array_tc = np.loadtxt("simplified_actuator_tc_long_data_cycle_0_2.csv", delimiter=",")
array_new = np.loadtxt("simplified_actuator_tc_long_data_cycle_1_2.csv", delimiter=",")
array_tc = np.concatenate((array_tc, array_new))
array_new = np.loadtxt("simplified_actuator_tc_long_data_cycle_2_2.csv", delimiter=",")
array_tc = np.concatenate((array_tc, array_new))

array_true = np.loadtxt("simplified_actuator_true_long_data_25.csv", delimiter=",")
time = np.linspace(0, 6, 6001, endpoint=True)

plt.plot(array_tc[:, 0], array_tc[:, 2], 'o', label="tc step w_2")
plt.plot(time, array_true[:, 1], 'o', label="true w_2")
plt.legend(loc="upper left")
plt.xlabel("Time(s)")
plt.ylabel("Angular Velocity")
plt.show()
