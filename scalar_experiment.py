# %%
import experts

from experts import problems
from experts.problems import ScalarExpertsProblem

import matplotlib.pyplot as plt

# %%
n_experts = 10
t_time = 100
beta = 0.01

# This is probably what you would expect
# when the experts and the outcome
# are all random sequences
# %%
A = ScalarExpertsProblem(n_experts, t_time)
result = A.mixture(beta)

# %%
plt.plot(result[0])
plt.show()

# %%
plt.plot(result[1])
plt.show()

# On the other hand,
# when the outcome sequence
# is one of the experts,
# the learning algorithm
# quickly follows the predictions
# of that leading expert

# %%
A = ScalarExpertsProblem(n_experts, t_time, outcomeAsExpert=1)
result = A.mixture(beta)

# %%
plt.plot(result[0])
plt.show()

# %%
plt.plot(result[1])
plt.show()
# %%
