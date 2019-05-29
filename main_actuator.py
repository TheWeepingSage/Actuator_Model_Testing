import numpy as np
import dynamics_actuator
import solver
import class_sat
import analytical_act_current as aac
import TorqueApplied
from constants_1U import CONTROL_STEP
import time as timer

start = timer.time()

sat = class_sat.Satellite(np.array([0, 0, 0, 1, 0, 0, 0]), 0)

sat.setRequiredTorque(0)
v_mag_i = np.array([1, 1, 1]) * 1e-4
sat.setMag_i(v_mag_i)
sat.setPos(np.array([1,1,1]))
sat.setVel(np.array([1,1,2]))
voltageRequired = TorqueApplied.ctrlTorqueToVoltage(sat)
v_duty_cycle = voltageRequired / 3.3

n = 15

voltageRequired = TorqueApplied.ctrlTorqueToVoltage(sat)
duty_cycle = voltageRequired/3.3
current_applied = np.zeros((3, 3))
edgeCurrentArray = aac.getEdgeCurrent(duty_cycle, np.zeros(3))
state_array = np.zeros((100001, 3))
state_array[0, :] = sat.getState()
for i in range(0, 100000):
    current_applied = aac.getCurrentList(duty_cycle, np.linspace(time[i], time[i+1], 3, endpoint=True), 3, np.zeros(3))
    torque_applied = TorqueApplied.currentToTorque(current_applied, sat)
    solver.rk4Quaternion(sat, dynamics_actuator.x_dot_BO, time[1]-time[0], torque_applied)
    state_array[i+1, :] = sat.getState()

np.savetxt("aac_test.csv", state_array[:, :], delimiter=",")
end = timer.time()
print(start - end)
