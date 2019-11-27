import numpy as np
from constants_1U import PWM_FREQUENCY, CONTROL_STEP, v_A_Torquer, No_Turns
import analytical_act_current as aac
import tc_step_sampling as tc
import time as timer

start = timer.time()


def w_dot_BI(current, b):   # defining the dynamics for the system
    v_mu = No_Turns*np.multiply(v_A_Torquer, current)   # mu = I*A*n
    v_w_dot = np.cross(v_mu, b)     # torque = mu x B
    return v_w_dot      # w_dot = torque


def getMag_b(t):     # defining the magnetic field in the body frame(constant in the body frame so that we can integrate analytically)
    v_mag_b = np.sin(np.array([1, 2, 3])*2*np.pi/1e-3*t)      # B =sin((1e-3, 2e-3, 3e-3)*2pi/T*t)
    return v_mag_b


I0 = np.zeros(3)    # initial current is 0
time_period = 1/PWM_FREQUENCY
num_steps = 5
w_initial = np.zeros((1, 4))
num_cycles_per_step = int(CONTROL_STEP/time_period)

for i in range(0, num_steps):

    time = np.array([i*CONTROL_STEP])      # initialising the time array for the control step
    duty = np.array([i+1, i+2, i+3]) * 1e-3*((-1)**i)     # initialising the duty cycle

    timeArr = tc.getTimeArr(duty)   # getting the time array for one PWM cycle
    num_instants_per_cycle = len(timeArr)
    for j in range(0, num_cycles_per_step):
        time = np.concatenate((time, timeArr + j*time_period + i*CONTROL_STEP))    # setting the time array for the whole step

    edgeCurrentArray = aac.getEdgeCurrent(duty, I0)     # getting the current at the edges

    w_array = np.zeros((len(time), 4))
    w_array[0] = w_initial
    w_array[:, 0] = time
    print("Step ", i + 1)
    for j in range(0, num_cycles_per_step):
        for k in range(j*num_instants_per_cycle, (j+1)*num_instants_per_cycle):
            intTimeArr1 = np.linspace(time[k]%2, time[k+1]%2, 3, endpoint=True)      # setting the time array for the integration step
            intTimeArr = np.linspace(time[k], time[k+1], 3, endpoint=True)
            currentArray = aac.getCurrentList(duty, intTimeArr1, 3, edgeCurrentArray)    # getting the current for the integration cycles
            h = time[k + 1] - time[k]
            k1 = w_dot_BI(currentArray[0], getMag_b(intTimeArr[0])) * h
            k2 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k3 = w_dot_BI(currentArray[1], getMag_b(intTimeArr[1])) * h
            k4 = w_dot_BI(currentArray[2], getMag_b(intTimeArr[2])) * h
            w_array[k + 1, 1:4] = w_array[k, 1:4]+(k1+2*k2+2*k3+k4)/6
    I0 = edgeCurrentArray[len(edgeCurrentArray) - 1]
    w_initial = np.array([w_array[len(w_array)-1]])
    np.savetxt("actuator_test_tc_sinusoid_step_%d.csv"%(i+1), w_array[:, :], delimiter=",")
end = timer.time()
print(end-start)