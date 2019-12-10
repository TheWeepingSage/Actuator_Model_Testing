import numpy as np
from qnv import quatRotate, quatDerBI
from constants_1U import v_A_Torquer, CONTROL_STEP, PWM_FREQUENCY, PWM_AMPLITUDE, Ixx, Ixy, Ixz, Iyy, Iyz, Izz
import analytical_act_current as aac


def w_dot(v_w, torque):  # w_dot = I^-1(torque + w x Iw)
    inertia_matrix = np.array([[Ixx, Ixy, Ixz],
                               [Ixy, Iyy, Iyz],
                               [Ixz, Iyz, Izz]])
    v_w_dot = np.dot(np.linalg.inv(inertia_matrix), (torque - np.cross(v_w, np.dot(inertia_matrix, v_w))))
    return v_w_dot


def appliedTorque(v_current, b_inertial, v_q):  # torque = m x B(body)
    b_body = quatRotate(v_q, b_inertial)    # rotating the field to the body frame
    torque = np.cross(np.multiply(v_A_Torquer, v_current), b_body)
    return torque


n = 100
v_duty_cycle = np.array([1.0, 1.0, 1.0]) * 1e-4   # duty cycle for the corresponding PWM
time_rising = np.linspace(0, int(1e-4/PWM_FREQUENCY), n, endpoint=False)
time_falling = np.linspace(int(1e-4/PWM_FREQUENCY), int(1/PWM_FREQUENCY), n, endpoint=False)
time_cycle = np.append(time_rising, time_falling)
time_array = time_cycle
for i in range(1, int(CONTROL_STEP*PWM_FREQUENCY)):
    time_array = np.append(time_array, time_cycle + i/PWM_FREQUENCY)
stateArray = np.zeros((len(time_array), 7))
stateArray[0] = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
v_b_applied = np.array([1.0, 2.0, 3.0]) * 1e-4    # b in the inertial frame
v_v_applied = v_duty_cycle * PWM_AMPLITUDE  # v = v_max * duty cycle
edgeCurrentArray = aac.getEdgeCurrent(v_duty_cycle, np.zeros(3))
for i in range(len(time_array)-1):
    state_i = stateArray[i, :]     # for indexing convenience
    time_rk4 = np.linspace(time_array[i], time_array[i+1], 3, endpoint=True)    # for convenience in accessing values
    h = float(time_array[i+1] - time_array[i])
    i_array = aac.getCurrentList(v_duty_cycle, time_rk4, 3, edgeCurrentArray)
    k1_q = quatDerBI(state_i[0:4], state_i[4:7]) * h     # rk4 algorithm
    k1_w = h * w_dot(state_i[4:7], appliedTorque(i_array[0], v_b_applied, state_i[0:4]))
    k2_q = quatDerBI(state_i[0:4] + k1_q/2.0, state_i[4:7]) * h
    k2_w = h * w_dot(state_i[4:7] + k1_w/2, appliedTorque(i_array[1], v_b_applied, state_i[0:4]))
    k3_q = quatDerBI(state_i[0:4] + k2_q / 2.0, state_i[4:7]) * h
    k3_w = h * w_dot(state_i[4:7] + k2_w / 2, appliedTorque(i_array[1], v_b_applied, state_i[0:4]))
    k4_q = quatDerBI(state_i[0:4] + k3_q, state_i[4:7]) * h
    k4_w = h * w_dot(state_i[4:7] + k3_w, appliedTorque(i_array[2], v_b_applied, state_i[0:4]))
    stateArray[i+1, 0:4] = state_i[0:4] + (k1_q + 2.0 * k2_q + 2.0 * k3_q + k4_q)/6.0  # update step for q
    stateArray[i+1, 0:4] /= np.linalg.norm(stateArray[i+1, 1:4])    # normalising q
    stateArray[i+1, 4:7] = state_i[4:7] + 1/6.0 * (k1_w + 2.0 * k2_w + 2.0 * k3_w + k4_w)     # update step for w
np.savetxt("actuator_pwm_state.csv", stateArray[:, :], delimiter=",")

