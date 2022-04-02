import numpy as np
import pytest

pytestmark = pytest.mark.dis

def _test_int_types(base, base_type, sub, sub_type):
    assert isinstance(sub, base_type)
    assert not isinstance(base, sub_type)

# I think this is faulty

def test_types_unit64_int():
    # np.uint64 is a type alias of int
    type_a = np.uint64
    type_b = int
    print(type_a, type_b)
    
    temp_a: type_a = 123
    temp_b: type_b = 321
    print(temp_a, temp_b)

    assert isinstance(temp_a, type_b)
    assert not isinstance(temp_b, type_a)
    
def test_types_unit64_int():
    # np.uint64 is a type alias of int
    type_a = np.uint64
    type_b = int
    print(type_a, type_b)
    
    temp_a: type_a = 123
    temp_b: type_b = 321
    print(temp_a, temp_b)

    assert isinstance(temp_a, type_b)
    assert not isinstance(temp_b, type_a)

    assert 0
