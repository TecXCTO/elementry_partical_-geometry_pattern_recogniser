"""
to build an evaluation wrapper around this function to scan a list of timestamps automatically, or do you want to change how the modulation parameters (ka, kf, kp) respond to your inputs.
"""
import numpy as np

def compute_wave_instant(t, f, A, phi1, phi2, phi3, ka=0.35, kf=15.0, kp=2.5):
    # Frequencies
    f1 = 0.5 * f
    f2 = f
    f3 = f
    f_res = 20.0 * f
    
    # Wave inputs at time t
    w1 = 2 * A * np.sin(2 * np.pi * f1 * t + np.radians(phi1))
    w2 = A * np.sin(2 * np.pi * f2 * t + np.radians(phi2))
    w3 = A * np.sin(2 * np.pi * f3 * t + np.radians(phi3))
    
    # AM Envelope
    am_envelope = 1.0 + ka * w1
    
    # FM and PM phase contributions
    # FM phase contribution uses the integral of sine which is -cos / (2*pi*f)
    fm_contrib = - (kf * A) / (2 * np.pi * f2) * np.cos(2 * np.pi * f2 * t + np.radians(phi2))
    pm_contrib = kp * w3
    
    # Total phase in radians
    total_phase_rad = (2 * np.pi * f_res * t) + fm_contrib + pm_contrib
    
    # Resulting wave amplitude value
    wave_val = am_envelope * np.cos(total_phase_rad)
    
    # Wrapped phase in degrees (0 to 360)
    phase_deg = np.degrees(total_phase_rad) % 360
    
    return {
        "t": t,
        "W1_val": w1,
        "W2_val": w2,
        "W3_val": w3,
        "AM_envelope": am_envelope,
        "Total_Phase_Deg": phase_deg,
        "Resulting_Wave_Val": wave_val
    }

# Quick test run for t = 0.05s, f = 1Hz, A = 1, phases = 0, 45, 90
res = compute_wave_instant(0.05, 1.0, 1.0, 0, 45, 90)
print(res)
