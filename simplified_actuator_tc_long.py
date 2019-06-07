import numpy as np
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, v_A_Torquer, No_Turns
import analytical_act_current as aac
import tc_step_sampling as tc
import time as timer

start = timer.time()


def w_dot_BI(current, b):
    v_mu = No_Turns*np.multiply(v_A_Torquer, current)
    v_w_dot = np.cross(v_mu, b)
    return v_w_dot


def getMag_b(time):
    v_mag_b = np.array([1, 2, 3])*1e-3
    return v_mag_b


I0 = np.zeros(3)
time_period = 1/PWM_FREQUENCY
num_steps = 8
w_array = np.zeros(4)
time = np.zeros(1)
num_cycles_per_step = int(CONTROL_STEP/time_period)

for i in range(0, num_steps):
    duty = np.array([i+1, (-1**i)*(i+2), i+3])*1e-3
    timeArr = tc.getTimeArr(duty)
    for j in range(0, num_cycles_per_step):
        time = np.concatenate((time, timeArr+j*time_period))
    num_instants_per_cycle = len(timeArr)
