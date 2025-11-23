import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

from data_functions import get_refractive_index
from optical_functions import two_layer_transmission

def error_function(measured_T_eff, calculated_T_eff):
    return np.sum((measured_T_eff - calculated_T_eff)**2)

# ----------------------------------------------------
# Settings
# ----------------------------------------------------
data_dir = r"C:\Users\Lucas\Desktop\Grad School Python\multi_layer_optics\data\ds_sipm_A"
file_pattern = os.path.join(data_dir, "RotBeamMap;*.csv")

d_scan = np.linspace(1.0, 2.0, 5000)  # thickness range in microns
n1 = 1.0   # air/vacuum

wavelength_min_nm = 700
wavelength_max_nm = 830

# Storage for heatmap
all_wavelengths_nm = []
error_matrix_rows = []   # each row = error(d) for one wavelength

# ----------------------------------------------------
# Loop over all files
# ----------------------------------------------------
file_paths = glob.glob(file_pattern)

for csv_path in tqdm(file_paths, desc="Processing files"):
    filename = os.path.basename(csv_path)

    # Parse wavelength from filename
    try:
        last_part = filename.split("__")[-1]  # "740nm.csv"
        wl_str = last_part.replace("nm.csv", "")
        wl_nm = int(wl_str)
    except:
        continue

    if not (wavelength_min_nm <= wl_nm <= wavelength_max_nm):
        continue

    # Load data
    data = pd.read_csv(csv_path)

    #data["current"] = data["current"] - (
    #    (data["current"].iloc[0] + data["current"].iloc[-1]) / 2
    #)

    currents = data["current"].iloc[1:-2].to_numpy()
    angles_deg = data["angle"].iloc[1:-2].to_numpy()
    angles_rad = np.deg2rad(angles_deg)

    currents = currents / np.max(currents)

    # Optical parameters for this wavelength
    wavelength_um = wl_nm / 1000.0
    k0 = 2 * np.pi / wavelength_um
    n2 = get_refractive_index("Quartz", wavelength_um)
    n3 = get_refractive_index("Silicon", wavelength_um)

    # -----------------------------------------------
    # Compute error(d) for ALL thickness values
    # -----------------------------------------------
    errors_for_this_wavelength = []

    for thickness in d_scan:
        T_eff_p, T_eff_s, T_eff_avg = two_layer_transmission(
            n1, n2, n3, angles_rad, k0, thickness
        )

        T_eff_avg = T_eff_avg / np.max(T_eff_avg)

        err = error_function(currents, T_eff_avg)
        errors_for_this_wavelength.append(err)

    all_wavelengths_nm.append(wl_nm)
    error_matrix_rows.append(errors_for_this_wavelength)

# ----------------------------------------------------
# Prepare heatmap matrix
# ----------------------------------------------------
all_wavelengths_nm = np.array(all_wavelengths_nm)
error_matrix = np.vstack(error_matrix_rows)    # shape = (num_wavelengths, num_thicknesses)

# Sort by wavelength
sort_idx = np.argsort(all_wavelengths_nm)
all_wavelengths_nm = all_wavelengths_nm[sort_idx]
error_matrix = error_matrix[sort_idx, :]

# ----------------------------------------------------
# Plot heatmap: x = thickness, y = wavelength
# ----------------------------------------------------
plt.figure(figsize=(10, 6))

extent = [
    d_scan[0], d_scan[-1],
    all_wavelengths_nm[0], all_wavelengths_nm[-1]
]

im = plt.imshow(
    error_matrix,
    aspect="auto",
    origin="lower",
    extent=extent,
    cmap="viridis"
)

plt.colorbar(im, label="Squared error")
plt.xlabel("Thickness (µm)")
plt.ylabel("Wavelength (nm)")
plt.title("Squared error as function of (thickness, wavelength)")
plt.tight_layout()
plt.show()
