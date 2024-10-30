import pytest

import experts

def test_digit():
    x = experts.utils.digit(13, 2, 1)
    assert x == 0
