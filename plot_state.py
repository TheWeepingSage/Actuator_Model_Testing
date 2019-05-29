import numpy as np
import matplotlib.pyplot as plt
from constants_1U import CONTROL_STEP, PWM_FREQUENCY
import analytical_act_current as aac
import class_sat
import TorqueApplied
import min_step_sampling
import tc_step_sampling

sat = class_sat.Satellite(np.array([0, 0, 0, 1, 0, 0, 0]), 0)

sat.setRequiredTorque(0)
Mag_i = np.array([1, 1, 1])*1e-4
sat.setMag_i(Mag_i)
sat.setPos(np.array([1, 1, 1]))
sat.setVel(np.array([1, 1, 2]))
voltageRequired = TorqueApplied.ctrlTorqueToVoltage(sat)
duty_cycle = voltageRequired/3.3

n = 15
num_cycles = 4

time1 = np.loadtxt("tcstep_time_array.csv", delimiter=",")

timeArr = min_step_sampling.getTime(duty_cycle, 15)
time2 = np.zeros(1)
for i in range(0, num_cycles):
    time2 = np.concatenate((time2, timeArr + i / PWM_FREQUENCY))

time3 = np.linspace(0, 0.004, 4001, endpoint=True)

time4 = np.linspace(0, 0.004, 40001, endpoint=True)

state1 = np.loadtxt("aac_test_tcstep.csv", delimiter=",")
state2 = np.loadtxt("aac_test_min_step.csv", delimiter=",")
state3 = np.loadtxt("aac_test_true.csv", delimiter=",")
state4 = np.loadtxt("aac_test_true_2.csv", delimiter=",")

plt.plot(time1, state1[0:125, 3], label="TC step sampling, state 3", color="red")
plt.plot(time2, state2[0:117, 3], label="minimum step sampling, state 3", color = "yellow")
plt.plot(time3, state3[:, 3], label="Fine sampling #1, state 3", color="blue")
plt.plot(time4, state4[:, 3], label="Fine Sampling #2, state 3", color="green")
plt.legend()
plt.show()
