import numpy as np
import matplotlib.pyplot as plt
from constants_1U import CONTROL_STEP, PWM_FREQUENCY
import analytical_act_current as aac

'''
v_duty_cycle = np.array([0.5, 0.7, 0.5])*1e-3
time_arr = np.linspace(0, int(CONTROL_STEP), 2000001, endpoint=True)
edge_current_array = aac.getEdgeCurrent(v_duty_cycle, I0=np.zeros(3))
current_array = aac.getCurrentList(v_duty_cycle, time_arr, 2000001, edge_current_array)
'''
n=5
time_array = np.linspace(0, CONTROL_STEP, int(n*CONTROL_STEP*PWM_FREQUENCY) + 1, endpoint=True)
stateArray = np.loadtxt("actuator_dc_state.csv", delimiter=",")
plt.plot(time_array, stateArray[:, 1])
plt.plot(time_array, stateArray[:, 0])
plt.ylabel("Quaternion component 1")
plt.title("q_1 vs Time for the actuator model")
plt.xlabel("time")
plt.show()
