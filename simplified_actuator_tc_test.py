import numpy as np
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, v_A_Torquer, No_Turns
import analytical_act_current as aac
import tc_step_sampling as tc
import time as timer

start = timer.time()

v_duty_cycle = np.array([3, 4, 5])*1e-3
timeArr = tc.getTimeArr(v_duty_cycle)
num_cycles = 2 * CONTROL_STEP * PWM_FREQUENCY

time = np.zeros(1)
for i in range(0, num_cycles):
    time = np.concatenate((time, timeArr + i / PWM_FREQUENCY))

num_instants = len(time)
w_array = np.zeros((num_instants, 4))
w_array[:, 0] = time
I0 = np.zeros(3)
edgeCurrentArray = aac.getEdgeCurrent(v_duty_cycle, I0)
currentArray = np.zeros((3, 3))


def w_dot_BI(current, b):
    v_mu = No_Turns*np.multiply(v_A_Torquer, current)
    v_w_dot = np.cross(v_mu, b)
    return v_w_dot


def getMag_b(time):
    v_mag_b = np.array([1, 2, 3])*1e-3*np.sin(time)
    return v_mag_b


for i in range(0, num_instants - 1):
    intTimeArr = np.linspace(time[i], time[i+1], 3, endpoint=True)
    currentArray = aac.getCurrentList(v_duty_cycle, intTimeArr, num_instants, edgeCurrentArray)
    h = time[i+1] - time[i]
    w_bIb = w_array[i, 1:3]
    # RK-4 routine
    k1 = w_dot_BI(currentArray[0], getMag_b(time[0]))
    k2 = w_dot_BI(currentArray[1], getMag_b(time[1]))
    k3 = w_dot_BI(currentArray[1], getMag_b(time[1]))
    k4 = w_dot_BI(currentArray[2], getMag_b(time[2]))
    w_array[i+1, 1:3] = w_bIb + (k1 + 2*k2 + 2*k3 + k4)/6

np.savetxt("simplified_actuator_tc_data.csv", w_array[:, :], delimiter=",")
end = timer.time()
print(end-start)
