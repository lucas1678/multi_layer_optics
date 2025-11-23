import numpy as np

def get_fresnel_coeffs(n1,n2,theta1,theta2):
    c1 = np.cos(theta1)
    c2 = np.cos(theta2)

    r_s = (n1*c1 - n2*c2)/(n1*c1 + n2*c2)
    r_p = (n2*c1 - n1*c2)/(n2*c1 + n1*c2)
    t_s = 2*n1*c1/(n1*c1 + n2*c2)
    t_p = 2*n1*c1/(n2*c1 + n1*c2)

    return r_s, r_p, t_s, t_p

def two_layer_transmission(n1,n2,n3,theta1,k0,d):
    theta2 = np.arcsin((n1*np.sin(theta1))/n2)
    theta3 = np.arcsin((n1*np.sin(theta1))/n3)

    delta = 2*k0*n2*d*np.cos(theta2)

    r_12s, r_12p, t_12s, t_12p = get_fresnel_coeffs(n1, n2, theta1, theta2)
    r_21s, r_21p, t_21s, t_21p = get_fresnel_coeffs(n2, n1, theta2, theta1)
    r_23s, r_23p, t_23s, t_23p = get_fresnel_coeffs(n2, n3, theta2, theta3)
    r_32s, r_32p, t_32s, t_32p = get_fresnel_coeffs(n3, n2, theta3, theta2)

    t_eff_p = (t_12p*t_23p)/(1+(r_12p*r_23p*np.exp(1j*delta)))
    T_eff_p = (n3*np.cos(theta3)/(n1*np.cos(theta1)))*(np.abs(t_eff_p))**2

    t_eff_s = (t_12s*t_23s)/(1+(r_12s*r_23s*np.exp(1j*delta)))
    T_eff_s = (n3*np.cos(theta3)/(n1*np.cos(theta1)))*(np.abs(t_eff_s))**2

    T_eff_avg = (T_eff_p+T_eff_s)/2

    return T_eff_p, T_eff_s, T_eff_avg