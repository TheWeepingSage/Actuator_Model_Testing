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

def getMag_b(time):     # defining the magnetic field in the body frame(constant in the body frame so that we can integrate analytically)
    v_mag_b = np.array([1, 2, 3])*1e-3      # B =(1e-3, 2e-3, 3e-3)
    return v_mag_b


I0 = np.zeros(3)    # initial current is 0
time_period = 1/PWM_FREQUENCY
num_steps = 5
num_points_per_cycle = 100
w_initial = np.zeros((1, 4))
num_cycles_per_step = int(CONTROL_STEP/time_period)

for i in range(0, num_steps):

    time = np.linspace(i*CONTROL_STEP, (i+1)*CONTROL_STEP, num_points_per_cycle*num_cycles_per_step, endpoint=True) # initialising the time array for the control step
    duty = np.array([i+1, i+2, i+3]) * 1e-3*((-1)**2)     # initialising the duty cycle

