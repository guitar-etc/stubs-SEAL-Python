from typing import Tuple, TypeAlias, TypeVar

import numpy as np

# from numpy.typing import NDArray

# VectorInt std::vector<std::int64_t>
# VectorDouble std::vector<double>

double = float
int = int
bool = bool

long = int

# TODO bound to np.generic_type
T = TypeVar("T")
# T = TypeVar("T")
# T = TypeVar("T", std.uint64_t, double)


class std:
    array: TypeAlias = tuple[T]
    string: TypeAlias = str
    vector: TypeAlias = list[T]
    size_t: TypeAlias = int
    # 여기도 numpy 뺄까?
    uint64_t: TypeAlias = np.uint64
    streamoff: TypeAlias = long


class py:
    array_t: TypeAlias = list[T]
    array_t_double: TypeAlias = array_t[double]
    # array_t_double: TypeAlias = NDArray[np.float64]
    # array_t: TypeAlias = NDArray[T]


# unique enough?
hash_block_type = Tuple[std.uint64_t, std.uint64_t, std.uint64_t, std.uint64_t]
parms_id_type = hash_block_type
