# %%
import experts

from experts import problems
from experts.problems import ScalarExpertsProblem

import numpy as np
import pandas as pd
import seaborn as sns

# %%
n_experts = 10
t_time = 100
beta = 0.01

experts_ = np.random.rand(t_time, n_experts)
outcomes = np.floor(2*np.random.rand(t_time))

# This is probably what you would expect
# when the experts and the outcome
# are all random sequences
# %%
A = ScalarExpertsProblem(n_experts, t_time, experts_, outcomes)
result = A.mixture(beta)

# %%
df = pd.DataFrame(dict(time = np.arange(100), loss = result[0]))
sns.relplot(x = "time", y = "loss", kind = "line", data = df)

# %%
df = pd.DataFrame(dict(time = np.arange(100), total_loss = result[1]))
sns.relplot(x = "time", y = "total_loss", kind = "line", data = df)

# On the other hand,
# when the outcome sequence
# is one of the experts,
# the learning algorithm
# quickly follows the predictions
# of that leading expert
# %%
A = ScalarExpertsProblem(n_experts, t_time,  experts_, outcomes, outcomeAsExpert=1, addNoise=1)
result = A.mixture(beta)

# %%
df = pd.DataFrame(dict(time = np.arange(100), loss = result[0]))
sns.relplot(x = "time", y = "loss", kind = "line", data = df)

# %%
df = pd.DataFrame(dict(time = np.arange(100), total_loss = result[1]))
sns.relplot(x = "time", y = "total_loss", kind = "line", data = df)

# %%
