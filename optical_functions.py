import numpy as np

def get_fresnel_coeffs(n1,n2,theta1,theta2):
    c1 = np.cos(theta1)
    c2 = np.cos(theta2)

    r_s = (n1*c1 - n2*c2)/(n1*c1 + n2*c2)
    r_p = (n2*c1 - n1*c2)/(n2*c1 + n1*c2)
    t_s = 2*n1*c1/(n1*c1 + n2*c2)
    t_p = 2*n1*c1/(n2*c1 + n1*c2)

    return r_s, r_p, t_s, t_p