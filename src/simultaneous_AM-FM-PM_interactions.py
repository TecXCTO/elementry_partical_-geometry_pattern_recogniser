# simultaneous AM-FM-PM interactions

import numpy as np
import matplotlib.pyplot as plt

# 1. Configuration Parameters
f_base = 1.0          # Base frequency (Hz)
f_carrier = 40.0 * f_base  # Target 40x accelerated frequency

# Define the three initial waves
# Wave 1 (AM): Half frequency, double amplitude
A1, f1, phase1 = 2.0, f_base / 2, 0.0
# Wave 2 (FM): Base frequency, standard amplitude
A2, f2, phase2 = 1.0, f_base, np.radians(45)
# Wave 3 (PM): Base frequency, standard amplitude, different phase
A3, f3, phase3 = 1.0, f_base, np.radians(90)

# Modulation sensitivities
ka = 0.35   # AM index
kf = 15.0   # FM index (Wideband sidebands)
kp = 2.5    # PM index (Phase deviation)

# 2. Time Array Generation (Sampling fast enough for 40x-80x waves)
t_start, t_end = 0.0, 2.0
fs = 20000  # Sampling rate (Hz)
t = np.linspace(t_start, t_end, int((t_end - t_start) * fs))

# 3. Compute Modulating Components
W1 = A1 * np.sin(2 * np.pi * f1 * t + phase1) # AM modulator
W2 = A2 * np.sin(2 * np.pi * f2 * t + phase2) # FM modulator
W3 = A3 * np.sin(2 * np.pi * f3 * t + phase3) # PM modulator

# FM requires integration of the message signal
W2_integral = -A2 * np.cos(2 * np.pi * f2 * t + phase2) / (2 * np.pi * f2)

# 4. Synthesize Combined AM-FM-PM Wave Function
am_envelope = 1.0 + ka * W1
instantaneous_phase_rad = (2 * np.pi * f_carrier * t) + (kf * W2_integral) + (kp * W3)
resulting_wave = am_envelope * np.cos(instantaneous_phase_rad)

# Convert total phase to wrapped degrees (0 to 360) for cycle tracking
phase_degrees = np.degrees(instantaneous_phase_rad) % 360

# 5. Plotting and Visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Top Subplot: The 40x Modulated Wave Output
ax1.plot(t, resulting_wave, label='Resulting Wave (40x f)', color='crimson', lw=1.2)
ax1.plot(t, am_envelope, '--', label='AM Envelope', color='black', alpha=0.5)
ax1.plot(t, -am_envelope, '--', color='black', alpha=0.5)
ax1.set_title('Simultaneous AM-FM-PM Wave Modulation (40x Frequency Shift)', fontsize=14)
ax1.set_ylabel('Amplitude')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# Bottom Subplot: Cycle Phase Tracking in Degrees
ax2.plot(t, phase_degrees, color='darkcyan', lw=1, label='Cycle Phase Angle')
ax2.set_title('Real-time Phase Tracking (Degrees per Wave Cycle)', fontsize=12)
ax2.set_xlabel('Time (Seconds)')
ax2.set_ylabel('Phase (Degrees)')
ax2.set_ylim(-10, 370)
ax2.set_yticks([0, 90, 180, 270, 360])
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# 6. Interactive Zoom and Image Capture Feature
# Zoom into a specific cycle window to see the 40x individual waves clearly
# Example: Zoom to view from 0.4 to 0.5 seconds
ax1.set_xlim(0.4, 0.5) 

# Save the captured image of this specific cycle window locally
output_filename = "wave_function_40x_capture.png"
plt.savefig(output_filename, dpi=300)
print(f"Success! Image of the wave cycles saved locally as: {output_filename}")

plt.show()
