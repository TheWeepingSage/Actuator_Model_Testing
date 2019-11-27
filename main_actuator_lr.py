import numpy as np
import dynamics_actuator
import solver
import class_sat
import TorqueApplied
from constants_1U import CONTROL_STEP, PWM_FREQUENCY, RESISTANCE, INDUCTANCE


n = 15
sat = class_sat.Satellite(np.array([0, 0, 0, 1, 0, 0, 0]), 0)
time = np.linspace(0, CONTROL_STEP, n*CONTROL_STEP*PWM_FREQUENCY+1, endpoint=True)
sat.setRequiredTorque(0)
v_mag_i = np.array([1, 1, 1]) * 1e-4
sat.setMag_i(v_mag_i)
sat.setPos(np.array([1,1,1]))
sat.setVel(np.array([1,1,2]))
voltageRequired = TorqueApplied.ctrlTorqueToVoltage(sat)
current_applied = np.zeros((3, 3))
state_array = np.zeros((len(time), 3))
state_array[0, :] = sat.getState()
for i in range(0, len(time)-1):
    i_time = np.linspace(time[i], time[i+1], 3, endpoint=True)
    current_applied = voltageRequired/RESISTANCE*(1-np.exp(-RESISTANCE*i_time/INDUCTANCE))
    torque_applied = TorqueApplied.currentToTorque(current_applied, sat)
    solver.rk4Quaternion(sat, dynamics_actuator.x_dot_BO, time[1]-time[0], torque_applied)
    state_array[i+1, :] = sat.getState()

np.savetxt("aac_test.csv", state_array[:, :], delimiter=",")

