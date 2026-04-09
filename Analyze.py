import numpy as np
import matplotlib.pyplot as plt

# ---- Neuron Parameters ----
dt = 0.0001          # time step (0.1 ms)
T = 0.5              # total simulation time (500 ms)
time = np.arange(0, T, dt)

V_rest = -70.0       # resting membrane potential (mV)
V_threshold = -55.0  # firing threshold (mV)
V_reset = -75.0      # reset potential after firing (mV)
R = 10.0             # membrane resistance (MOhm)
tau = 0.02           # membrane time constant (20 ms)

# ---- Input Current ----
# Simulating a constant input current to the neuron
I_input = 2.0        # input current (nA)

# ---- Simulation ----
V = V_rest           # start at resting potential
voltage_trace = []   # record voltage over time
spike_times = []     # record when spikes occur

for t in time:
    # Integrate - accumulate input
    dV = (dt / tau) * (-(V - V_rest) + R * I_input)
    V += dV
    
    # Fire - if threshold crossed, reset
    if V >= V_threshold:
        spike_times.append(t)
        V = V_reset
    
    voltage_trace.append(V)

print(f"Total spikes fired: {len(spike_times)}")
print(f"Firing rate: {len(spike_times) / T:.1f} Hz")

# ---- Plot ----
fig, axes = plt.subplots(2, 1, figsize=(12, 7))

# Voltage trace
axes[0].plot(time * 1000, voltage_trace, color='steelblue', linewidth=0.8)
axes[0].axhline(V_threshold, color='red', linestyle='--', 
                linewidth=1, label='Threshold (-55 mV)')
axes[0].axhline(V_rest, color='gray', linestyle=':', 
                linewidth=1, label='Resting potential (-70 mV)')
axes[0].set_ylabel('Membrane Potential (mV)')
axes[0].set_title('Integrate-and-Fire Neuron Simulation')
axes[0].legend()

# Spike raster
axes[1].eventplot([s * 1000 for s in spike_times], 
                  color='red', linewidths=1.5)
axes[1].set_xlabel('Time (ms)')
axes[1].set_ylabel('Spikes')
axes[1].set_title(f'Spike Train — {len(spike_times)} spikes at {len(spike_times)/T:.1f} Hz')

plt.tight_layout()
plt.savefig('integrate_and_fire.png', dpi=150)
print("Plot saved as integrate_and_fire.png")