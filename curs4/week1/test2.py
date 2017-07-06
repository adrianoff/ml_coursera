from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.proportion import samplesize_confint_proportion
import numpy as np

print round(proportion_confint(1, 50, method="wilson")[0], 4)
n_samples = int(np.ceil(samplesize_confint_proportion(0.5, 0.01)))
print n_samples
