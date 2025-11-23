import matplotlib.pyplot as plt
import numpy as np
from data_functions import get_refractive_index
from optical_functions import get_fresnel_coeffs

wavelength = 0.500 # microns
k0 = 2*np.pi/wavelength 
n1 = 1.0 # vacuum
n2 = get_refractive_index("Quartz", wavelength)
n3 = get_refractive_index("Silicon", wavelength)

theta1 = np.linspace(0, np.pi/2, 10000)
theta1_degrees = theta1*180/np.pi
theta2 = np.arcsin((n1*np.sin(theta1))/n2)
theta3 = np.arcsin((n1*np.sin(theta1))/n3)

r_12s, r_12p, t_12s, t_12p = get_fresnel_coeffs(n1, n2, theta1, theta2)
r_21s, r_21p, t_21s, t_21p = get_fresnel_coeffs(n2, n1, theta2, theta1)

r_23s, r_23p, t_23s, t_23p = get_fresnel_coeffs(n2, n3, theta2, theta3)
r_32s, r_32p, t_32s, t_32p = get_fresnel_coeffs(n3, n2, theta3, theta2)

layer_thicknesses = np.linspace(1.1, 1.2, 20) # microns
for layer_thickness in layer_thicknesses:


    delta = 2*k0*n2*layer_thickness*np.cos(theta2)

    t_eff_p = (t_12p*t_23p)/(1+(r_12p*r_23p*np.exp(1j*delta)))
    T_eff_p = (n3*np.cos(theta3)/(n1*np.cos(theta1)))*(np.abs(t_eff_p))**2

    t_eff_s = (t_12s*t_23s)/(1+(r_12s*r_23s*np.exp(1j*delta)))
    T_eff_s = (n3*np.cos(theta3)/(n1*np.cos(theta1)))*(np.abs(t_eff_s))**2

    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8,4))

    ax1.plot(theta1_degrees, T_eff_p, label=r"$T_p$")
    ax1.plot(theta1_degrees, T_eff_s, label=r"$T_s$")
    ax2.plot(theta1_degrees, (T_eff_p + T_eff_s)/2, label=r"$T_{avg}$", color='green')

    ax1.legend()
    ax2.set_title('Unpolarized Transmission')
    ax1.set_title('Polarized Transmission')

    fig.suptitle(f'Vacuum/Quartz/Silicon Transmission ({wavelength*1000}nm), d={layer_thickness:.2f}μm)')

    plt.ylabel('Transmission')
    plt.xlabel('Angle of Incidence (deg)')
    plt.show()