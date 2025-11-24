import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import glob
import re
from data_functions import get_refractive_index
from optical_functions import two_layer_transmission

def error_function(measured_T_eff, calculated_T_eff):
    return np.sum((measured_T_eff - calculated_T_eff)**2)

def extract_wavelength_from_filename(filename):
    """Extract wavelength in nm from filename like 'xxx__760nm.csv'"""
    match = re.search(r'(\d{3})nm\.csv$', filename)
    if match:
        return int(match.group(1))
    return None

def process_wavelength_file(filepath, thickness_range, n1=1.0):
    """Process a single CSV file for a given wavelength"""
    # Extract wavelength from filename
    wavelength_nm = extract_wavelength_from_filename(filepath)
    if wavelength_nm is None:
        return None, None
    
    wavelength_um = wavelength_nm / 1000.0  # Convert nm to microns
    k0 = 2 * np.pi / wavelength_um
    
    # Read and process data
    data = pd.read_csv(filepath)
    data["current"] = data["current"] - ((data["current"].iloc[0] + data["current"].iloc[-1]) / 2)
    currents = data["current"].iloc[1:-2].to_numpy()
    currents = currents / np.max(currents)
    angles = data["angle"].iloc[1:-2].to_numpy()
    angles_rad = angles * (np.pi) / 180
    
    # Get refractive indices
    n2 = get_refractive_index("Quartz", wavelength_um)
    n3 = get_refractive_index("Silicon", wavelength_um)
    
    # Calculate error for each thickness
    error_func_vals = []
    for thickness in thickness_range:
        T_eff_p, T_eff_s, T_eff_avg = two_layer_transmission(n1, n2, n3, angles_rad, k0, thickness)
        T_eff_avg = T_eff_avg / np.max(T_eff_avg)
        error_val = error_function(currents, T_eff_avg)
        error_func_vals.append(error_val)
    
    return wavelength_nm, np.array(error_func_vals)

# Main script
data_folder = "/home/lubackes/Desktop/python_codes/multi_layer_optics/data/ds_sipm_A"
csv_files = glob.glob(f"{data_folder}/*nm.csv")

print(f"Found {len(csv_files)} CSV files")

# Define thickness range
d = np.linspace(1.0, 2.5, 5000)

# Store results
results = {}

# Process each file
print("Processing files...")
for filepath in tqdm(csv_files):
    wavelength_nm, errors = process_wavelength_file(filepath, d)
    if wavelength_nm is not None:
        results[wavelength_nm] = errors
        print(f"  Processed {wavelength_nm}nm")

# Sort wavelengths
wavelengths = sorted(results.keys())
print(f"\nProcessed wavelengths: {wavelengths} nm")

# Create 2D array for heatmap
error_matrix = np.zeros((len(wavelengths), len(d)))
for i, wl in enumerate(wavelengths):
    error_matrix[i, :] = results[wl]

# Create heatmap
plt.figure(figsize=(12, 8))
plt.imshow(error_matrix, aspect='auto', origin='lower', 
           extent=[d[0], d[-1], wavelengths[0], wavelengths[-1]],
           cmap='hot', interpolation='bilinear')
plt.colorbar(label='Error Squared')
plt.xlabel('Thickness (μm)', fontsize=12)
plt.ylabel('Wavelength (nm)', fontsize=12)
plt.title('Error Squared: Wavelength vs Thickness', fontsize=14)
plt.tight_layout()
plt.savefig('wavelength_thickness_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Optional: Create contour plot as alternative visualization
plt.figure(figsize=(12, 8))
X, Y = np.meshgrid(d, wavelengths)
levels = 20
contour = plt.contourf(X, Y, error_matrix, levels=levels, cmap='hot')
plt.colorbar(contour, label='Error Squared')
plt.xlabel('Thickness (μm)', fontsize=12)
plt.ylabel('Wavelength (nm)', fontsize=12)
plt.title('Error Squared Contours: Wavelength vs Thickness', fontsize=14)
plt.tight_layout()
plt.savefig('wavelength_thickness_contours.png', dpi=300, bbox_inches='tight')
plt.show()

# Find minimum error for each wavelength
print("\nMinimum error thickness for each wavelength:")
for i, wl in enumerate(wavelengths):
    min_idx = np.argmin(error_matrix[i, :])
    min_thickness = d[min_idx]
    min_error = error_matrix[i, min_idx]
    print(f"  {wl}nm: d = {min_thickness:.3f} μm, error² = {min_error:.6f}")