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
n_1=5
n_2 = 100
time_array_dc = np.linspace(0, CONTROL_STEP, int(n_1*CONTROL_STEP*PWM_FREQUENCY) + 1, endpoint=True)
time_rising = np.linspace(0, int(1e-4/PWM_FREQUENCY), n_2, endpoint=False)
time_falling = np.linspace(int(1e-4/PWM_FREQUENCY), int(1/PWM_FREQUENCY), n_2, endpoint=False)
time_cycle = np.append(time_rising, time_falling)
time_array_pwm = time_cycle
for i in range(1, int(CONTROL_STEP*PWM_FREQUENCY)):
    time_array_pwm = np.append(time_array_pwm, time_cycle + i / PWM_FREQUENCY)
stateArray_dc = np.loadtxt("actuator_dc_state.csv", delimiter=",")
stateArray_pwm = np.loadtxt("actuator_pwm_state.csv", delimiter=",")
# plt.plot(time_array_dc[:], stateArray_dc[:, 3], label="DC quaternion")
plt.plot(time_array_pwm[:], stateArray_pwm[:, 0], label="PWM Quaternion")
plt.ylabel("Quaternion component 1")
plt.legend(loc="upper right")
plt.title("q_1 vs Time for the actuator model")
plt.xlabel("time")
plt.show()
