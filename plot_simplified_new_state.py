import numpy as np
import matplotlib.pyplot as plt

control_step = 2

array_tc = np.loadtxt("simplified_actuator_tc_long_data_step_1.csv", delimiter=",")
for i in range(4):
    array_temp = np.loadtxt("simplified_actuator_tc_long_data_step_%d.csv"%(i+2), delimiter=",")
    array_tc = np.vstack((array_tc, array_temp))

array_true = np.loadtxt("simplified_actuator_true_long_data_five_steps.csv", delimiter=",")
true_time_array = np.linspace(0, 10, 10001, endpoint=True)

plt.plot(array_tc[:, 0], array_tc[:, 1], label="computed w_0")
plt.plot(true_time_array, array_true[:, 0], label="true w_0")
plt.legend(loc='upper left')
plt.xlabel("time")
plt.ylabel("angular velocity")
plt.show()