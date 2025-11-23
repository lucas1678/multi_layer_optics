import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from data_functions import get_refractive_index
from optical_functions import two_layer_transmission

def error_function(measured_T_eff, calculated_T_eff):
    return np.sum((measured_T_eff - calculated_T_eff)**2)

data = pd.read_csv(r"C:\Users\Lucas\Desktop\Grad School Python\multi_layer_optics\data\ds_sipm_A\RotBeamMap;142__2025_9_12_1-38-04__T5C__760nm.csv")
data["current"] = data["current"] - ((data["current"].iloc[0]+data["current"].iloc[-1])/2)
currents = data["current"].iloc[1:-2].to_numpy()
currents = currents/np.max(currents)
angles = data["angle"].iloc[1:-2].to_numpy()
angles_rad = angles*(np.pi)/180



wavelength = 0.760 # microns
k0 = 2*np.pi/wavelength 
n1 = 1.0 # vacuum
n2 = get_refractive_index("Quartz", wavelength)
n3 = get_refractive_index("Silicon", wavelength)

d = np.linspace(1.0,2.5,5000)
error_func_vals = []

for thickness in tqdm(d):
    T_eff_p, T_eff_s, T_eff_avg = two_layer_transmission(n1,n2,n3,angles_rad,k0,thickness)
    T_eff_avg = T_eff_avg / np.max(T_eff_avg)
    error_val = error_function(currents, T_eff_avg)
    error_func_vals.append(error_val)

    #plt.title(f"Error = {error_val}, Thickness = {thickness}um")
    #plt.plot(angles, currents, label='Data')
    #plt.plot(angles, T_eff_avg, label='Fit', linestyle="--")
    #plt.show()

best_thickness = d[np.argmin(error_func_vals)]
print(f'Best Thickness is: {best_thickness} giving an squared error of {np.min(error_func_vals)}')
plt.plot(d, error_func_vals)
plt.show()


T_eff_p, T_eff_s, T_eff_avg = two_layer_transmission(n1,n2,n3,angles_rad,k0,best_thickness)
T_eff_avg = T_eff_avg / np.max(T_eff_avg)

plt.title(f"Best Guess")
plt.plot(angles, currents, label='Data')
plt.plot(angles, T_eff_avg, label='Fit', linestyle="--")
plt.legend()
plt.show()