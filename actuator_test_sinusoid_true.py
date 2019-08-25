import analytical_act_current as aac
from constants_1U import CONTROL_STEP, PWM_FREQUENCY, PWM_AMPLITUDE as V_max, v_A_Torquer, RESISTANCE as R, INDUCTANCE as L, No_Turns
import numpy as np


t_p = 1/PWM_FREQUENCY
w_array = np.zeros((1, 3))
num_steps = 5
I0 = np.zeros(3)
num_cycles_per_step = int(CONTROL_STEP/t_p)


def int_exp_sin(k, w, t):
    return (w - w*np.cos(w*t)*np.exp(-k*t) - k*np.sin(w*t)*np.exp(-k*t))/(k**2+w**2)


def int_exp_cos(k, w, t):
    return 1/k*(1-np.cos(w*t)*np.exp(-k*t)) - w/k*int_exp_sin(k, w, t)


def int_m1_x_b1(n1, t1, I_0):
    k_exp = R/L
    w_sin = 2*np.pi*n1/t_p
    res = V_max/R/w_sin*(1-np.cos(w_sin*t1)) - (V_max/R-I_0)*int_exp_sin(k_exp, w_sin, t1)
    res2 = (V_max/R -(V_max/R-I_0)*np.exp(-k_exp*t1))
    res2 *= (np.cos(w_sin*t1)*int_exp_sin(k_exp, w_sin, t_p-t1) - np.sin(w_sin*t1)*int_exp_cos(k_exp, w_sin, t_p-t1))
    return (res + res2)*v_A_Torquer[0]


def m_x_b(n1, n2, v_duty_cycle, v_edgeCurrent):
    t1 = v_duty_cycle[n1-1]
    t2 = v_duty_cycle[n2-1]
    I1 = v_edgeCurrent[n1-1]
    I2 = v_edgeCurrent[n2-1]
    return int_m1_x_b1(n1, t1, I1)-int_m1_x_b1(n2, t2, I2)


def integral_current_step(v_duty_cycle, v_edgeCurrent):
    int1 = m_x_b(2, 3, v_duty_cycle, v_edgeCurrent)
    int2 = m_x_b(3, 1, v_duty_cycle, v_edgeCurrent)
    int3 = m_x_b(1, 2, v_duty_cycle, v_edgeCurrent)
    return np.array([int1, int2, int3])


for i in range(0, num_steps):
    duty = np.array([i+1, i+2, i+3]) * 1e-3*((-1)**2)
    edgeCurrent = aac.getEdgeCurrent(duty, I0)
    for j in range(0, num_cycles_per_step):
        angular_velocity = w_array[i*num_cycles_per_step+j] + integral_current_step(duty, edgeCurrent[2*j])
        w_array = np.vstack((w_array, angular_velocity))
    I0 = edgeCurrent[len(edgeCurrent) - 1]
np.savetxt("actuator_test_sinusoid_true.csv", w_array[:, :], delimiter=",")
