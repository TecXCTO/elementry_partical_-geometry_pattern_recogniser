"""
It features a standalone calculation function to pull the exact values of all three input waves, the current AM envelope boundary, the resulting wave amplitude, and the exact cycle phase position in degrees for any specific instant in time or cycle you choose.
"""
import numpy as np

def calculate_wave_at_instant(t, f_base, A_base, phi1_deg, phi2_deg, phi3_deg, ka=0.35, kf=15.0, kp=2.5):
    """
    Calculates the exact state of all waves and the combined output at any precise second (t).
    All starting phases should be provided in degrees.
    """
    # 1. Establish frequencies based on conditions
    f1 = 0.5 * f_base       # Lowest frequency wave
    f2 = 1.0 * f_base       # Upper wave 2
    f3 = 1.0 * f_base       # Upper wave 3
    f_res = 20.0 * f_base   # Resulting carrier frequency (40x of f1, 20x of f2/f3)
    
    # Convert starting phases from degrees to radians for numpy
    p1 = np.radians(phi1_deg)
    p2 = np.radians(phi2_deg)
    p3 = np.radians(phi3_deg)
    
    # 2. Compute individual phase differences (in degrees)
    diff_12 = (phi2_deg - phi1_deg) % 360
    diff_23 = (phi3_deg - phi2_deg) % 360
    diff_13 = (phi3_deg - phi1_deg) % 360
    
    # 3. Compute instantaneous value of the 3 input waves at time 't'
    w1_val = 2 * A_base * np.sin(2 * np.pi * f1 * t + p1)  # Double amplitude
    w2_val = A_base * np.sin(2 * np.pi * f2 * t + p2)
    w3_val = A_base * np.sin(2 * np.pi * f3 * t + p3)
    
    # 4. Compute the resulting dynamic AM amplitude envelope
    am_envelope = 1.0 + ka * w1_val
    
    # 5. Compute the instantaneous modulation phase shifts 
    # (Note: FM integrates the sine wave message into a negative cosine wave)
    fm_phase_shift = - (kf * A_base) / (2 * np.pi * f2) * np.cos(2 * np.pi * f2 * t + p2)
    pm_phase_shift = kp * w3_val
    
    # Total phase inside the final wave argument (in Radians)
    total_phase_rad = (2 * np.pi * f_res * t) + fm_phase_shift + pm_phase_shift
    
    # 6. Extract the localized cycle angle position (Wrapped 0 to 360 degrees)
    resulting_phase_deg = np.degrees(total_phase_rad) % 360
    
    # 7. Final synthesized wave function value
    resulting_wave_val = am_envelope * np.cos(total_phase_rad)
    
    # Print out a clean data snapshot
    print(f"=== WAVE SNAPSHOT AT INSTANT t = {t} seconds ===")
    print(f"Base Input Frequency: {f_base} Hz | Resulting Output Frequency: {f_res} Hz")
    print(f"Fixed Input Phase Differences: Δ1-2 = {diff_12}°, Δ2-3 = {diff_23}°, Δ1-3 = {diff_13}°")
    print("-" * 50)
    print(f"Wave 1 Instant Value (AM Modulator) : {w1_val:.4f}")
    print(f"Wave 2 Instant Value (FM Modulator) : {w2_val:.4f}")
    print(f"Wave 3 Instant Value (PM Modulator) : {w3_val:.4f}")
    print("-" * 50)
    print(f"Current AM Envelope Limit (+/-)     : {am_envelope:.4f}")
    print(f"Resulting Wave Position In Cycle    : {resulting_phase_deg:.2f}°")
    print(f"Final Combined Output Amplitude     : {resulting_wave_val:.4f}\n")
    
    return resulting_wave_val

# ==========================================
# EXAMPLE RUN
# ==========================================
# Set up parameters: Base frequency = 1Hz, Base Amplitude = 1.0
# Starting Phases in degrees: Wave 1 = 0°, Wave 2 = 45°, Wave 3 = 90°
target_time = 0.05  # Change this to inspect any exact time slice you want

calculate_wave_at_instant(
    t=target_time, 
    f_base=1.0, 
    A_base=1.0, 
    phi1_deg=0.0, 
    phi2_deg=45.0, 
    phi3_deg=90.0
)
