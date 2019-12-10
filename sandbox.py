import numpy as np
import matplotlib.pyplot as plt
# import scipy.fftpack
from constants_1U import PWM_FREQUENCY, RESISTANCE, INDUCTANCE


def a_n(n):
    numerator = 13.2*(np.sin(n * np.pi * 1e-4)**2)  # *RESISTANCE
    denominator = n*np.sqrt(RESISTANCE**2 + (2*np.pi*PWM_FREQUENCY*n*INDUCTANCE)**2)*np.pi
    return numerator / denominator


n_array = np.linspace(1, 40000, 40000, endpoint=True)
plt.plot(n_array*PWM_FREQUENCY, a_n(n_array))
plt.xlabel("Frequency")
plt.ylabel("Amplitude of current")
plt.grid()
plt.title("Coefficients of harmonics in the periodic part of the current")
plt.show()


'''
# Number of samplepoints
N = 60000
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
print(yf)
fig, ax = plt.subplots()
ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.show()
'''
