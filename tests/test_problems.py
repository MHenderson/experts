import pytest

import experts
from experts.problems import ScalarExpertsProblem

def test_setting_name():
    jack_account = "Matthew Henderson"
    assert jack_account == "Matthew Henderson"