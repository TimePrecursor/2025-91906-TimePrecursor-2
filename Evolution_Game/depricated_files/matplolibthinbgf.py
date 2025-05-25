import numpy as np
import matplotlib.pyplot as plt

# Parameters
mu = 0         # Mean
sigma = 100    # Standard deviation
n = 10000      # Number of samples

# Generate Gaussian-distributed data
data = np.random.normal(mu, sigma, n)

# Plotting
plt.figure(figsize=(8, 5))
plt.hist(data, bins=200, density=True, color='skyblue', edgecolor='black', alpha=0.7)
plt.title(f'Gaussian Distribution\nMean = {mu}, Std Dev = {sigma}', fontsize=14)
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.grid(True)

# Optional: add the theoretical curve
from scipy.stats import norm
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
plt.plot(x, norm.pdf(x, mu, sigma), 'r--', label='Theoretical PDF')
plt.legend()

plt.show()
