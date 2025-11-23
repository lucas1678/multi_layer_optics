import numpy as np
import pandas as pd

QUARTZ_DATA = "/home/lubackes/Desktop/python_codes/multi_layer_optics/data/quartz_index_of_refraction_vals.csv"
SILICON_DATA = "/home/lubackes/Desktop/python_codes/multi_layer_optics/data/Franta-100K_Si_refractive_index.csv"

def get_refractive_index(material, wavelength): #wavelength in microns (um)
    if material == "Quartz":
        quartz_data = pd.read_csv(QUARTZ_DATA)
        interpolated_index = np.interp(wavelength, quartz_data['wl(um)'], quartz_data['n'])
    elif material == "Silicon":
        silicon_data = pd.read_csv(SILICON_DATA)
        interpolated_index = np.interp(wavelength, silicon_data['wl(um)'], silicon_data['n'])
    else:
        raise ValueError(f"{material} is not a recognized material!")

    return interpolated_index