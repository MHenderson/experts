# %%
import experts

from experts import problems
from experts.problems import VectorExpertsProblem

import matplotlib.pyplot as plt

# %%
vector_length = 15
n_experts = 20
t_time = 25
beta = 0.1

# %%
A = VectorExpertsProblem(vector_length, n_experts, t_time, 1, 1, 1, 1)

result = A.mixture(beta)

# %%
plt.plot(result[0])
plt.show()
# %%
