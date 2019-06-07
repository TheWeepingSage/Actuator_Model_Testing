import analytical_act_current as aac
from constants_1U import PWM_FREQUENCY, PWM_AMPLITUDE as V_max, v_A_Torquer, RESISTANCE as R, INDUCTANCE as L, No_Turns
import numpy as np
import matplotlib.pyplot as plt

duty = np.array([3, 4, 5])*1e-3
t_p = 1/PWM_FREQUENCY
edgeCurrent_1 = aac.getEdgeCurrent(duty, np.zeros(3))
edgeCurrent_2 = aac.getEdgeCurrent(duty, edgeCurrent_1[len(edgeCurrent_1)-1, :])
w_array = np.zeros((len(edgeCurrent_1), 1))
for i in range(0, 2000):
    w_array[i + 1] = w_array[i] + V_max/R*t_p*(2*duty[0]-1*duty[1])
    w_array[i + 1] = w_array[i + 1] - V_max/R*L/R*(2*np.exp(-t_p*(1 - duty[0])*R/L)-1*np.exp(-t_p*(1-duty[1])*R/L))
    w_array[i + 1] = w_array[i + 1] + L/R * (2*edgeCurrent_1[2*(i%2000), 0]-1*edgeCurrent_1[2*(i%2000), 1])*(1 - np.exp(-R*t_p/L))
for i in range(2000, 4000):
    w_array[i + 1] = w_array[i] + V_max/R*t_p*(2*duty[0]-1*duty[1])
    w_array[i + 1] = w_array[i + 1] - V_max/R*L/R*(2*np.exp(-t_p*(1 - duty[0])*R/L)-1*np.exp(-t_p*(1-duty[1])*R/L))
    w_array[i + 1] = w_array[i + 1] + L/R * (2*edgeCurrent_2[2*(i%2000), 0]-1*edgeCurrent_2[2*(i%2000), 1])*(1 - np.exp(-R*t_p/L))
w_array = w_array * v_A_Torquer[0]*1e-3*No_Turns
np.savetxt("simplified_actuator_true_data_3.csv", w_array[:, :], delimiter=",")
