import analytical_act_current as aac
from constants_1U import CONTROL_STEP, PWM_FREQUENCY, PWM_AMPLITUDE as V_max, v_A_Torquer, RESISTANCE as R, INDUCTANCE as L, No_Turns
import numpy as np


t_p = 1/PWM_FREQUENCY
w_array = np.zeros((1, 3))
num_steps = 8
I0 = np.zeros(3)
num_cycles_per_step = int(CONTROL_STEP/t_p)


def integral_current_step(v_duty_cycle, v_edgeCurrent):
    res = V_max*t_p*v_duty_cycle
    res = res - V_max*L/R/R*(np.exp(-R*t_p/L*(1-v_duty_cycle)) + np.exp(-R*t_p/L))
    res = res + v_edgeCurrent*L/R*(1-np.exp(-R*t_p/L))
    res = np.cross(res, np.array([1, 2, 3])*1e-3)
    return res


for i in range(0, num_steps):
    duty = np.array([i+1, (-1**i)*(i+2), i+3])*1e-3
    edgeCurrent = aac.getEdgeCurrent(duty, I0)
    for j in range(0, num_cycles_per_step):
        angular_velocity = w_array[i*num_cycles_per_step+j] + integral_current_step(duty, edgeCurrent[2*j])
        w_array = np.vstack((w_array, angular_velocity))
    I0 = edgeCurrent[len(edgeCurrent) - 1]
w_array = w_array * v_A_Torquer[0]*No_Turns
np.savetxt("simplified_actuator_true_long_data_2.csv", w_array[:, :], delimiter=",")