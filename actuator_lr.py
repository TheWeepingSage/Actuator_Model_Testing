import numpy as np
from qnv import quatRotate, quatDerBI
from constants_1U import v_A_Torquer, CONTROL_STEP, PWM_FREQUENCY, PWM_AMPLITUDE, RESISTANCE, INDUCTANCE, Ixx, Ixy, Ixz, Iyy, Iyz, Izz


def w_dot(v_w, torque):  # w_dot = I^-1(torque + w x Iw)
    inertia_matrix = np.array([[Ixx, Ixy, Ixz],
                               [Ixy, Iyy, Iyz],
                               [Ixz, Iyz, Izz]])
    v_w_dot = np.linalg.inv(inertia_matrix)*(torque - np.cross(v_w, inertia_matrix*v_w))
    return v_w_dot


def appliedTorque(v_current, b_inertial, v_q):  # torque = m x B(body)
    b_body = quatRotate(v_q, b_inertial)    # rotating the field to the body frame
    torque = np.cross(np.multiply(v_A_Torquer, v_current), b_body)
    return torque


n = 5
time_array = np.linspace(0, CONTROL_STEP, n*CONTROL_STEP*PWM_FREQUENCY + 1, endpoint=True)
stateArray = np.zeros((len(time_array), 7))
stateArray[0] = np.array([0, 0, 0, 1, 0, 0, 0])
v_b_applied = np.array([1, 2, 3]) * 1e-4    # b in the inertial frame
v_duty_cycle = np.array([1, 1, 1]) * 1e-4   # duty cycle for the corresponding PWM
v_v_applied = v_duty_cycle * PWM_AMPLITUDE  # v = v_max * duty cycle
for i in range(len(time_array)-1):
    state_i = stateArray[i]     # for indexing convenience
    time_rk4 = np.linspace(time_array[i], time_array[i+1], 3, endpoint=True)    # for convenience in accessing values
    h = time_array[i+1] - time_array[i]
    i_array = np.zeros(3,3)
    factor_exp = (1-np.exp(-time_rk4*RESISTANCE/INDUCTANCE))
    i_array[:, 0] = v_v_applied[0] * factor_exp
    i_array[:, 1] = v_v_applied[1] * factor_exp     # i_k = V_k/R(1-e^(-Rt/L))
    i_array[:, 2] = v_v_applied[2] * factor_exp
    k1_q = h * quatDerBI(state_i[0:4], stateArray[4:7])     # rk4 algorithm
    k1_w = h * w_dot(state_i[4:6], appliedTorque(i_array[0], v_b_applied, state_i[0:4]))
    k2_q = h * quatDerBI(state_i[0:4] + k1_q/2, state_i[4:7])
    k2_w = h * w_dot(state_i[4:7] + k1_w/2, appliedTorque(i_array[1], v_b_applied, state_i[0:4]))
    k3_q = h * quatDerBI(state_i[0:4] + k2_q / 2, state_i[4:7])
    k3_w = h * w_dot(state_i[4:7] + k2_w / 2, appliedTorque(i_array[1], v_b_applied, state_i[0:4]))
    k4_q = h * quatDerBI(state_i[0:4] + k3_q, state_i[4:7])
    k4_w = h * w_dot(state_i[4:7] + k3_w, appliedTorque(i_array[2], v_b_applied, state_i[0:4]))
    stateArray[i+1, 0:4] = state_i[0:4] + 1/6 * (k1_q + 2 * k2_q + 2 * k3_q + k4_q)     # update step
    stateArray[i+1, 4:7] = state_i[4:7] + 1/6 * (k1_w + 2 * k2_w + 2 * k3_w + k4_w)
np.savetxt("actuator_dc_state.csv", delimiter=",")
