import numpy as np
import matplotlib.pyplot as plt

control_step = 2
'''
array_tc = np.loadtxt("simplified_actuator_tc_long_data_cycle_0_2.csv", delimiter=",")
array_new = np.loadtxt("simplified_actuator_tc_long_data_cycle_1_2.csv", delimiter=",")
array_tc = np.concatenate((array_tc, array_new))
array_new = np.loadtxt("simplified_actuator_tc_long_data_cycle_2_2.csv", delimiter=",")
array_tc = np.concatenate((array_tc, array_new))

array_true = np.loadtxt("simplified_actuator_true_long_data_.csv", delimiter=",")
time = np.linspace(0, 6, 6001, endpoint=True)

plt.plot(array_tc[:, 0], array_tc[:, 2], 'o', label="tc step w_2")
plt.plot(time, array_true[:, 1], 'o', label="true w_2")
plt.legend(loc="upper left")
plt.xlabel("Time(s)")
plt.ylabel("Angular Velocity")
plt.show()
'''

array_new = np.loadtxt("simplified_actuator_tc_long_data_cycle_0_4.csv", delimiter=",")
array_new_2 = np.loadtxt("simplified_actuator_tc_long_data_cycle_1_4.csv", delimiter=",")
array_new = np.concatenate((array_new, array_new_2))
array_true = np.loadtxt("simplified_actuator_true_long_data_3.csv", delimiter=",")
time_arr = np.linspace(0, 4, 4001, endpoint=False)
array_old = np.loadtxt("simplified_actuator_tc_data_3.csv", delimiter=",")
array_true_2 = np.loadtxt("simplified_actuator_true_data_6.csv", delimiter=",")
plt.plot(array_old[:, 0], array_old[:, 1], label="old w_0")
plt.plot(array_new[:, 0], array_new[:, 1], label="new w_0")
plt.plot(time_arr, -array_true_2, label="true_old w_0")
plt.plot(time_arr, array_true[:, 0], label="true w_0")
plt.legend(loc="upper left")
plt.show()
w_final_tc = array_old[len(array_old)-1, 1:4]
w_final_true = array_true[len(array_true)-1, :]
factor = np.divide(w_final_true, w_final_tc)
print(factor)