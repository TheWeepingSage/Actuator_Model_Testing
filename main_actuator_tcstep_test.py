import numpy as np
import dynamics_actuator
import solver
import class_sat
import analytical_act_current as aac
import TorqueApplied
from constants_1U import CONTROL_STEP, PWM_FREQUENCY
import time as timer
import tc_step_sampling

start = timer.time()

sat = class_sat.Satellite(np.array([0, 0, 0, 1, 0, 0, 0]), 0)

sat.setRequiredTorque(0)
Mag_i = np.array([1,1,1])*1e-4
sat.setMag_i(Mag_i)
sat.setPos(np.array([1,1,1]))
sat.setVel(np.array([1,1,2]))
voltageRequired = TorqueApplied.ctrlTorqueToVoltage(sat)
v_duty_cycle = voltageRequired / 3.3

n = 15

num_cycles = 4
timeArr = tc_step_sampling.getTimeArr(v_duty_cycle)
num_instants = num_cycles * len(timeArr) + 1
time = np.zeros(1)
for i in range(0, num_cycles):
    time = np.concatenate((time, timeArr + i / PWM_FREQUENCY))

current_applied = np.zeros((3, 3))
edgeCurrentList = aac.getEdgeCurrent(v_duty_cycle, np.zeros(3))
state_array = np.zeros((num_instants + 1, 7))
start_1 = timer.time()
state_array[0] = sat.getState()
print(num_instants)

for i in range(0, num_instants - 1):
    current_applied = aac.getCurrentList(v_duty_cycle, np.linspace(time[i], time[i + 1], 3, endpoint=True), 3, np.zeros(3))
    torque_applied = TorqueApplied.currentToTorque(current_applied, sat)
    solver.rk4Quaternion(sat, dynamics_actuator.x_dot_BO, time[i+1]-time[i], torque_applied)
    state_array[i+1, :] = sat.getState()
    print(sat.getState())
    if i % (num_instants / 100) == 0:
        print(i/(num_instants / 100), "%")
        end_1 = timer.time()
        print(end_1 - start_1)
np.savetxt("aac_test_tcstep.csv", state_array[:, :], delimiter=",")
end = timer.time()
print(-start + end)




