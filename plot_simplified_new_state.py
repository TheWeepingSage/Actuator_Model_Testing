import numpy as np
import matplotlib.pyplot as plt

control_step = 2
array_tc = np.loadtxt("simplified_actuator_tc_long_data_cycle_0.csv", delimiter=",")
for i in range(1, 8):
    array_tc_temp = np.loadtxt("simplified_actuator_tc_long_data_cycle_%d.csv" % i, delimiter=",")

array_true = np.loadtxt("simplified_actuator_true_long_data_2.csv", delimiter=",")
time = np.linspace(0, 4, 16001, endpoint=True)

plt.plot(array_tc[:, 0], array_tc[:, 2], label="tc step w_2")
plt.plot(time, array_true[:], label="true w_2")
plt.legend(loc="upper left")
plt.xlabel("Time(s)")
plt.ylabel("Angular Velocity")
plt.show()
