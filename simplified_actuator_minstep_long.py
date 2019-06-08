import numpy as np
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, v_A_Torquer, No_Turns
import analytical_act_current as aac
import min_step_sampling as minstep
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
    timeArr = minstep.getTime(duty, 15)
    num_instants_per_cycle = len(timeArr)
    for j in range(0, num_cycles_per_step):
        time = np.concatenate((time, timeArr+j*time_period))
    edgeCurrentArray = aac.getEdgeCurrent(duty, I0)
    for j in range(0, num_cycles_per_step):
        print("step ", i+1, " cycle ", j)
        for k in range(j*num_instants_per_cycle, (j+1)*num_instants_per_cycle):
            intTimeArr = np.linspace(time[k] % time_period, time[k+1] % time_period, 3, endpoint=True)
            currentArray = aac.getCurrentList(duty, intTimeArr, 3, edgeCurrentArray)
            h = time[k + 1] - time[k]
            k1 = w_dot_BI(currentArray[0], getMag_b(intTimeArr[0])) * h
            k2 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k3 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k4 = w_dot_BI(currentArray[2], getMag_b(intTimeArr[2])) * h
            angular_velocity_new = np.concatenate((time[k+1], (w_array[i*num_cycles_per_step+k, 1:4]+(k1+2*k2+2*k3+k4)/6)))
            w_array = np.vstack((w_array, angular_velocity_new))
    I0 = edgeCurrentArray[len(edgeCurrentArray) - 1]

np.savetxt("simplified_actuator_minstep_long_data.csv", w_array[:, :], delimiter=",")
end = timer.time()
print(end-start)
