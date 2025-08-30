import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Load your Excel data
df = pd.read_csv('pedal_map_data.xlsx')

# Get unique pedal values (sorted)
pedal_values = sorted(df['pedal'].unique())

plt.figure(figsize=(10, 6))

# Plot accel vs velocity for each pedal value


fig, ax = plt.subplots(figsize=(14, 10))  # Wider to fit legend below

# Plot for each pedal value
for pedal in pedal_values:
    subset = df[df['pedal'] == pedal]
    ax.plot(np.array(subset['velocity']),
            np.array(subset['acceleration']),
            label=f'Pedal={pedal:.2f}')

# Place the legend **below** the plot, in multiple columns
ax.legend(loc='upper center',
          bbox_to_anchor=(0.5, -0.15),  # Below the plot
          ncol=6,                       # Adjust this based on how many pedal levels you have
          fontsize='small',
          frameon=True)

# Axis labels, limits, and title
ax.set_ylim(-10, 10)
ax.set_xlabel('Current Velocity in m/s')
ax.set_ylabel('Acceleration in m/s²')
ax.set_title('Pedal Map')
ax.grid(True)

plt.tight_layout()  # Automatically adjust plot to fit labels
plt.show()


