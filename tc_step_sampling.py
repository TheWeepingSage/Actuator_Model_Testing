import numpy as np
from constants_1U import PWM_FREQUENCY, RESISTANCE, INDUCTANCE

def getTimeArr(duty_cycle):
    peak_time = np.abs(duty_cycle)/PWM_FREQUENCY
    time_constant = INDUCTANCE / RESISTANCE * 4.606
    time_prev = np.linspace(peak_time / 4, peak_time, 3, endpoint=False)
    time_tc = np.linspace(peak_time + time_constant/3, peak_time + time_constant, 3, endpoint=True)
    time_post = np.linspace((peak_time + time_constant)*2/3 + 1/PWM_FREQUENCY/3, 1/PWM_FREQUENCY*0.9999, 3, endpoint=True)
    time_arr = np.concatenate((time_prev, time_tc, time_post))
    time_arr1 = time_arr.flatten()
    time_arr1 = np.concatenate((time_arr1, np.unique(peak_time)))
    time_arr1 = np.append(time_arr1, 1/PWM_FREQUENCY)
    return np.unique(time_arr1)
