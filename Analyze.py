import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

n_channels = 8
sampling_rate = 10000

# Load data
data = np.fromfile('d5331/d533101.dat', dtype=np.int16)
data = data.reshape(-1, n_channels)

# Look at first 3 seconds
seconds = 3
samples = seconds * sampling_rate
snippet = data[:samples, 0]  # Channel 0 only

# Step 1 - Highpass filter to remove slow drifts and isolate spikes
def highpass_filter(data, cutoff=300, fs=10000):
    b, a = butter(4, cutoff / (fs/2), btype='high')
    return filtfilt(b, a, data)

filtered = highpass_filter(snippet)

# Step 2 - Detect spikes by finding where signal crosses threshold
threshold = -4 * np.std(filtered)  # 4 standard deviations below mean
print("Spike threshold:", round(threshold, 2))

# Find spike locations
spike_indices = np.where(filtered < threshold)[0]

# Remove duplicates (same spike detected multiple times)
min_distance = 30  # samples (3ms refractory period)
spikes = [spike_indices[0]]
for idx in spike_indices[1:]:
    if idx - spikes[-1] > min_distance:
        spikes.append(idx)

spike_times = np.array(spikes) / sampling_rate
print(f"Number of spikes detected: {len(spikes)}")
print(f"Spike times (seconds): {spike_times[:10]}")

# Step 3 - Plot the filtered signal with spikes marked
time = np.arange(samples) / sampling_rate

plt.figure(figsize=(14, 5))
plt.plot(time, filtered, linewidth=0.5, color='steelblue', label='Filtered signal')
plt.axhline(threshold, color='red', linestyle='--', linewidth=1, label=f'Threshold')
plt.plot(spike_times, filtered[(np.array(spikes))], 'v', 
         color='red', markersize=8, label=f'{len(spikes)} spikes detected')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Spike Detection - CA1 Channel 0')
plt.legend()
plt.tight_layout()
plt.savefig('spike_detection.png', dpi=150)
print("Plot saved as spike_detection.png")