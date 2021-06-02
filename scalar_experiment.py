# %%
import experts

from experts import problems
from experts.problems import ScalarExpertsProblem

import numpy as np
import pandas as pd
import seaborn as sns

import random

# %%
n_experts = 10
t_time = 100
beta = 0.01

# create a matrix of experts,
# each is just a random sequence
# of length t_time
# so we don't need to also pass t_time,
# or n_expers
# both are given by the dimension of this matrix
experts_ = np.random.rand(t_time, n_experts)

outcomes = np.floor(2*np.random.rand(t_time))

# This is probably what you would expect
# when the experts and the outcome
# are all random sequences
# %%
A = ScalarExpertsProblem(n_experts, t_time, experts_, outcomes)
result = A.mixture(beta)

# %%
df = pd.DataFrame(
    dict(
        time = np.arange(100),
        loss = result["learner-loss"],
        total_loss = result["learner-loss"].cumsum()
        )
    )

sns.relplot(x = "time", y = "loss", kind = "line", data = df)

# %%
sns.relplot(x = "time", y = "total_loss", kind = "line", data = df)

# On the other hand,
# when the outcome sequence
# is one of the experts,
# the learning algorithm
# quickly follows the predictions
# of that leading expert
# %%

# add outcomes as one of the experts
experts_[:, n_experts - 1] = outcomes

# with some gaussian noise (should do this first?)
for t in range(t_time):
  a = random.gauss(0, 0.01)
  if 0 <= a + experts_[t, n_experts - 1] <= 1:
    experts_[t, n_experts - 1] = a + experts_[t, n_experts - 1]

A = ScalarExpertsProblem(n_experts, t_time,  experts_, outcomes)
result = A.mixture(beta)

# %%
df = pd.DataFrame(
    dict(
        time = np.arange(100),
        loss = result["learner-loss"],
        total_loss = result["learner-loss"].cumsum()
    )
)

sns.relplot(x = "time", y = "loss", kind = "line", data = df)

# %%
sns.relplot(x = "time", y = "total_loss", kind = "line", data = df)

# %%
