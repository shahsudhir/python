import matplotlib.pyplot as plt

x_values = range(1, 1001)
y_values = [x**2 for x in x_values]

plt.style.use('seaborn-v0_8')  # Or 'ggplot', 'default', etc.
fig, ax = plt.subplots()  # Corrected: Call subplots() as a function
ax.scatter(x_values, y_values, c=y_values, s=10)

# Set the range for axes
ax.axis([0, 1100, 0, 1100000])

plt.show()
