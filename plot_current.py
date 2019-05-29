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

num_cycles = int(CONTROL_STEP * PWM_FREQUENCY)
num_instants = int(num_cycles * n * 2)

timeArr = tc_step_sampling.getTimeArr(duty_cycle)
time1 = np.zeros(1)
for i in range(0, num_cycles):
    time1 = np.concatenate((time1, timeArr + i / PWM_FREQUENCY))

timeArr = min_step_sampling.getTime(duty_cycle, 15)
time2 = np.zeros(1)
for i in range(0, num_cycles):
    time2 = np.concatenate((time2, timeArr + i / PWM_FREQUENCY))

time3 = np.linspace(0, CONTROL_STEP, 1000001, endpoint=True)

current1 = aac.getCurrentList(duty_cycle, time1, len(time1), I0=np.zeros(3))
current2 = aac.getCurrentList(duty_cycle, time2, len(time2), I0=np.zeros(3))
current3 = aac.getCurrentList(duty_cycle, time3, len(time3), I0=np.zeros(3))

plt.plot(time1, current1[:, 0], label="tc method [0]")
#plt.plot(time2, current2[:, 0], label= "min step method [0]")
plt.plot(time3, current3[:, 0], label="true [0]")
plt.legend()
plt.xlabel = "time(s)"
plt.ylabel = "current(A)"
plt.show()

plt.plot(time1, current1[:, 1], label="tc method [1]")
#plt.plot(time2, current2[:, 1], label= "min step method [1]")
plt.plot(time3, current3[:, 1], label="true [1]")
plt.legend()
plt.xlabel = "time(s)"
plt.ylabel = "current(A)"
plt.show()

plt.plot(time1, current1[:, 2], label="tc method [2]")
#plt.plot(time2, current2[:, 2], label= "min step method [2]")
plt.plot(time3, current3[:, 2], label="true [2]")
plt.legend()
plt.xlabel = "time(s)"
plt.ylabel = "current(A)"
plt.show()
