# %%
import experts

from experts import problems
from experts.problems import ScalarExpertsProblem

import matplotlib.pyplot as plt

# %%
n_experts = 3
t_time = 100
beta = 0.2

# %%
A = ScalarExpertsProblem(n_experts, t_time, 1, 1, 1, 1, 1)
result = A.mixture(beta)[0]

# %%
plt.plot(result)
plt.show()

# %%
