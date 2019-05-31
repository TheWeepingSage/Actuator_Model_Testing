import numpy as np
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, v_A_Torquer, No_Turns
import analytical_act_current as aac
import tc_step_sampling as tc
import time as timer

start = timer.time()

v_duty_cycle = np.array([3, 4, 5])*1e-3
timeArr = tc.getTimeArr(v_duty_cycle)
num_instants_per_cycle = len(timeArr)
num_cycles = int(2 * CONTROL_STEP * PWM_FREQUENCY)

time = np.zeros(1)
for i in range(0, num_cycles):
    time = np.concatenate((time, timeArr + i / PWM_FREQUENCY))

w_array = np.zeros((len(time), 4))
w_array[:, 0] = time
I0 = np.zeros(3)


def w_dot_BI(current, b):
    v_mu = No_Turns*np.multiply(v_A_Torquer, current)
    v_w_dot = np.cross(v_mu, b)
    return v_w_dot


def getMag_b(time):
    v_mag_b = np.array([1, 2, 3])*1e-3*np.sin(time)
    return v_mag_b


for j in range(0, 2):
    for k in range(0, int(num_cycles / 2)):
        edgeCurrentArray = aac.getEdgeCurrent(v_duty_cycle, I0)
        currentArray = np.zeros((3, 3))
        for i in range(k * num_instants_per_cycle, (k + 1) * num_instants_per_cycle):
            intTimeArr = np.linspace(time[i], time[i+1], 3, endpoint=True)
            currentArray = aac.getCurrentList(v_duty_cycle, intTimeArr, 3, edgeCurrentArray)
            h = time[i+1] - time[i]
            w_bIb = w_array[i, 1:4]
            # RK-4 routine
            k1 = w_dot_BI(currentArray[0], getMag_b(intTimeArr[0])) * h
            k2 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k3 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k4 = w_dot_BI(currentArray[2], getMag_b(intTimeArr[2])) * h
            w_array[i+1, 1:3] = w_bIb + (k1 + 2*k2 + 2*k3 + k4)/6
        I0 = edgeCurrentArray[len(edgeCurrentArray) - 1]


np.savetxt("simplified_actuator_tc_data.csv", w_array[:, :], delimiter=",")
end = timer.time()
print(end-start)
