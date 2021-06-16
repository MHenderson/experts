import pytest

import experts
from experts.problems import ScalarExpertsProblem

def test_prediction_function():
    A = ScalarExpertsProblem(1, 0)
    x = A.predictionFunction(1, 0.1)
    assert x == 1