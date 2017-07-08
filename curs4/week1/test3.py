from scipy.stats import norm
import scipy
import numpy as np
print norm.ppf(0.9985)

z = scipy.stats.norm.ppf(1 - 0.05 / 2.)
p2 = float(104) / 11037
p1 = float(189) / 11034

left_boundary = (p1 - p2) - z * np.sqrt(p1 * (1 - p1) / 11037 + p2 * (1 - p2) / 11034)
right_boundary = (p1 - p2) + z * np.sqrt(p1 * (1 - p1) / 11037 + p2 * (1 - p2) / 11034)

print right_boundary
