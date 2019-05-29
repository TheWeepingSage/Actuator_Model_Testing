import numpy as np
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, v_A_Torquer, No_Turns
import analytical_act_current as aac
import tc_step_sampling as tc

w_bIb = np.zeros(3)
v_mag_b = np.array([1, 2, 3])*1e-3
v_duty_cycle = np.array([3, 4, 5])*1e-3
timeArr = tc.getTimeArr(v_duty_cycle)
num_cycles = 5

time = np.zeros(1)
for i in range(0, num_cycles):
    time = np.concatenate((time, timeArr + i / PWM_FREQUENCY))

num_instants = len(time)
w_array = np.zeros((num_instants, 4))
w_array[:, 0] = time
I0 = np.zeros(3)
edgeCurrentArray = aac.getEdgeCurrent(v_duty_cycle, I0)
currentArray = np.zeros((3, 3))

for i in range(0, num_instants):
    intTimeArr = np.linspace(time[i], time[i+1], 3, endpoint=True)
    currentArray = aac.getCurrentList(v_duty_cycle, intTimeArr, num_instants, edgeCurrentArray)
    h = time[i+1] - time[i]
