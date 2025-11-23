import matplotlib.pyplot as plt
import numpy as np
from data_functions import get_refractive_index
from optical_functions import get_fresnel_coeffs

wavelength = 0.500 # microns
n1 = 1.0 # vacuum
n2 = get_refractive_index("Quartz", wavelength)
n3 = get_refractive_index("Silicon", wavelength)

theta1 = np.linspace(0, np.pi/2, 1000)
theta1_degrees = theta1*180/np.pi
theta2 = np.arcsin((n1*np.sin(theta1))/n2)
r_s, r_p, t_s, t_p = get_fresnel_coeffs(n1, n2, theta1, theta2)

R_p = np.abs(r_p)**2
#T_p = 1 - R_p #also works, at least when extinction is 0? or no TIR?
T_p = ((n2*np.cos(theta2))/(n1*np.cos(theta1)))*(np.abs(t_p))**2
R_s = np.abs(r_s)**2
#T_s = 1 - R_s #also works, at least when extinction is 0? or no TIR?
T_s = ((n2*np.cos(theta2))/(n1*np.cos(theta1)))*(np.abs(t_s))**2





fig, (ax1,ax2) = plt.subplots(1,2, figsize=(8,4))

ax1.plot(theta1_degrees, r_s, label=r"$r_s$")
ax1.plot(theta1_degrees, r_p, label=r"$r_p$")
ax1.plot(theta1_degrees, t_p, label=r"$t_p$", linestyle="--")
ax1.plot(theta1_degrees, t_s, label=r"$t_s$", linestyle="--")

ax2.plot(theta1_degrees, R_p, label=r"R_p")
ax2.plot(theta1_degrees, T_p, label=r"T_p")
ax2.plot(theta1_degrees, R_s, label=r"R_s", linestyle="--")
ax2.plot(theta1_degrees, T_s, label=r"T_s", linestyle="--")


ax1.legend()
ax1.set_xlabel('Angle of Incidence (deg)')

plt.show()

#print(f"r_s = {r_s}\nr_p = {r_p}\nt_s = {t_s}\nt_p = {t_p}")