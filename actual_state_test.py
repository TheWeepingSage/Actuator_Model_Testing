import numpy as np
import matplotlib.pyplot as plt
from constants_1U import CONTROL_STEP, PWM_FREQUENCY
import class_sat
import TorqueApplied

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



