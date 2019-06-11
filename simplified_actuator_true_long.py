import analytical_act_current as aac
from constants_1U import CONTROL_STEP, PWM_FREQUENCY, PWM_AMPLITUDE as V_max, v_A_Torquer, RESISTANCE as R, INDUCTANCE as L, No_Turns
import numpy as np


t_p = 1/PWM_FREQUENCY
w_array = np.zeros(1)
num_steps = 8
I0 = np.zeros(3)
num_cycles_per_step = int(CONTROL_STEP/t_p)

for i in range(0, num_steps):
    duty = np.array([i+1, (-1**i)*(i+2), i+3])*1e-3
    edgeCurrent = aac.getEdgeCurrent(duty, I0)
    for j in range(0, num_cycles_per_step):
        angular_velocity = w_array[i*num_cycles_per_step+j] + V_max/R*t_p*(1*duty[2]-3*duty[0])
        angular_velocity = angular_velocity + (V_max*L/R/R)*np.exp(-t_p*R/L)*(1-3)
        angular_velocity = angular_velocity - V_max/R*L/R*(1*np.exp(-t_p*(1 - duty[2])*R/L)-3*np.exp(-t_p*(1-duty[0])*R/L))
        angular_velocity = angular_velocity + L/R*(1*edgeCurrent[2*(i%2000), 2]-3*edgeCurrent[2*(i%2000), 0])*(1 - np.exp(-R*t_p/L))
        w_array = np.vstack((w_array, angular_velocity))
    I0 = edgeCurrent[len(edgeCurrent) - 1]
w_array = w_array * v_A_Torquer[0]*1e-3*No_Turns
np.savetxt("simplified_actuator_true_long_data_2.csv", w_array[:, :], delimiter=",")