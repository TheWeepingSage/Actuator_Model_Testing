import numpy as np
from qnv import quatRotate, quatDerBI
from constants_1U import v_A_Torquer, CONTROL_STEP, PWM_FREQUENCY


def w_dot(v_w, mat_I, torque):
    v_w_dot = np.linalg.inv(mat_I)*torque + np.cross(v_w, mat_I*w)
    return v_w_dot
def appliedTorque(v_current, b_Inertial, v_q):
    b_Body = quatRotate(v_q, b_Inertial)
    torque = np.cross(np.multiply(v_A_Torquer, v_current), b_Body)
    return torque


n = 5
time_array = np.linspace(0, CONTROL_STEP, n*CONTROL_STEP*PWM_FREQUENCY)
stateArray = np.zeros(len(CONTROL_STEP), 7)
stateArray[0] = np.array([0, 0, 0, 1, 0, 0, 0])
v_applied = np.array([1,2,3]) * 1e-4

