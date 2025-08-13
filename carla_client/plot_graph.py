import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Load your Excel data
df = pd.read_csv('pedal_map_data.xlsx')

# Get unique pedal values (sorted)
pedal_values = sorted(df['pedal'].unique())

plt.figure(figsize=(10, 6))

# Plot accel vs velocity for each pedal value
for pedal in pedal_values:
    subset = df[df['pedal'] == pedal]
    plt.plot(np.array(subset['velocity']),np.array(subset['acceleration']), label=f'Pedal={pedal:.2f}')
plt.ylim(-20, 20)
plt.xlabel('Initial Velocity (m/s)')
plt.ylabel('Acceleration (m/s²)')
plt.title('Acceleration vs Initial Velocity for different Pedal Values')
plt.legend()
plt.grid(True)
plt.show()
