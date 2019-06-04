import analytical_act_current as aac
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, PWM_AMPLITUDE, v_A_Torquer, RESISTANCE, INDUCTANCE
import numpy as np
import matplotlib.pyplot as plt

v_duty_cycle = np.array([3, 4, 5])*1e-3
time_period = 1/PWM_FREQUENCY
edgeCurrentArray_1 = aac.getEdgeCurrent(v_duty_cycle, np.zeros(3))
edgeCurrentArray_2 = aac.getEdgeCurrent(v_duty_cycle, edgeCurrentArray_1[len(edgeCurrentArray_1)-1, :])
w_array = np.zeros((len(edgeCurrentArray_1), 3))
for i in range(0, 2000):
    w_array[i + 1] = w_array[i] + PWM_AMPLITUDE/RESISTANCE*time_period*(v_duty_cycle[1]-v_duty_cycle[2])
    w_array[i + 1] = w_array[i + 1] - PWM_AMPLITUDE/RESISTANCE*INDUCTANCE/RESISTANCE*(np.exp(-time_period*(1 - v_duty_cycle[1])*RESISTANCE/INDUCTANCE)-np.exp(-time_period*(1-v_duty_cycle[2])*RESISTANCE/INDUCTANCE))
    w_array[i + 1] = w_array[i + 1] + INDUCTANCE/RESISTANCE * (edgeCurrentArray_1[2*(i%2000), 1]-edgeCurrentArray_1[2*(i%2000), 2])*(1 - np.exp(-RESISTANCE*time_period/INDUCTANCE))
    print(w_array[i+1]*1e-3)
for i in range(2000, 4000):
    w_array[i + 1] = w_array[i] + PWM_AMPLITUDE/RESISTANCE*time_period*(v_duty_cycle[1]-v_duty_cycle[2])
    w_array[i + 1] = w_array[i + 1] - PWM_AMPLITUDE/RESISTANCE*INDUCTANCE/RESISTANCE*(np.exp(-time_period*(1 - v_duty_cycle[1])*RESISTANCE/INDUCTANCE)-np.exp(-time_period*(1-v_duty_cycle[2])*RESISTANCE/INDUCTANCE))
    w_array[i + 1] = w_array[i + 1] + INDUCTANCE/RESISTANCE * (edgeCurrentArray_2[2*(i%2000), 1]-edgeCurrentArray_1[2*(i%2000), 2])*(1 - np.exp(-RESISTANCE*time_period/INDUCTANCE))
    print(w_array[i+1]*1e-3)
w_array = w_array * v_A_Torquer[0]*1e-3
print(w_array[len(w_array)-1])
