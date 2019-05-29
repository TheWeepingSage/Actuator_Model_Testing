import numpy as np
from constants_1U import PWM_FREQUENCY

def getTime(duty_cycle, n):
    v_duty_cycle = np.sort(np.abs(duty_cycle))
    if v_duty_cycle[0]!=0:
        time_a = v_duty_cycle[0]/ PWM_FREQUENCY
        timeStep_h = time_a / n
        time_b = v_duty_cycle[2] / PWM_FREQUENCY
        timeStep_l = (1 / PWM_FREQUENCY - time_b) / n
        timeArr_h = np.linspace(timeStep_h, time_b, int(time_b / timeStep_h), endpoint=True)
        timeArr_l = np.linspace(timeStep_l + time_b, 1 / PWM_FREQUENCY, n, endpoint=True)
        timeArr = np.concatenate((timeArr_h, timeArr_l))
    elif v_duty_cycle[1]!=0:
        time_a = v_duty_cycle[0] / PWM_FREQUENCY
        timeStep_h = time_a / n
        time_b = v_duty_cycle[1] / PWM_FREQUENCY
        timeStep_l = (1 / PWM_FREQUENCY - time_b) / n
        timeArr_h = np.linspace(timeStep_h, time_b, int(time_b / timeStep_h), endpoint=True)
        timeArr_l = np.linspace(timeStep_l + time_b, 1 / PWM_FREQUENCY, n, endpoint=True)
        timeArr = np.concatenate((timeArr_h, timeArr_l))
    elif v_duty_cycle[2]!=0:
        time_a = v_duty_cycle[1] / PWM_FREQUENCY
        timeStep_h = time_a / n
        time_b = v_duty_cycle[2] / PWM_FREQUENCY
        timeStep_l = (1 / PWM_FREQUENCY - time_b) / n
        timeArr_h = np.linspace(timeStep_h, time_b, int(time_b / timeStep_h), endpoint=True)
        timeArr_l = np.linspace(timeStep_l + time_b, 1 / PWM_FREQUENCY, n, endpoint=True)
        timeArr = np.concatenate((timeArr_h, timeArr_l))
    else:
        timeArr = np.linspace(1 / PWM_FREQUENCY / 2 / n, 1/PWM_FREQUENCY, 2*n, endpoint=True)
    return timeArr
