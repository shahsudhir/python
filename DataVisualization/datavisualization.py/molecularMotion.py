import matplotlib.pyplot as plt
from random_walk import RandomWalk

# Make a random walk
rw = RandomWalk(5000)
rw.fill_walk()

# Plot the points
plt.style.use('classic')
fig, ax = plt.subplots()
ax.plot(rw.x_values, rw.y_values, linewidth=1)
ax.set_aspect('equal')

# Emphasize the first and last points
ax.plot(0, 0, 'go', label='Start')  # Green start point
ax.plot(rw.x_values[-1], rw.y_values[-1], 'ro', label='End')  # Red end point

# Add labels and title
ax.set_title("Random Walk Simulating Pollen Grain Motion")
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")
ax.legend()

plt.show()