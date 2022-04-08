from typing import Tuple, TypeAlias, TypeVar

import numpy as np
from numpy.typing import NDArray

# VectorInt std::vector<std::int64_t>
# VectorDouble std::vector<double>

double = float
long = int
int = int
bool = bool


class std:
    array: TypeAlias = tuple
    string: TypeAlias = str
    vector: TypeAlias = list
    size_t: TypeAlias = int
    uint64_t: TypeAlias = np.uint64
    streamoff: TypeAlias = long


# T = TypeVar("T")
# T = TypeVar("T", std.uint64_t, double)


class py:
    array_t_double: TypeAlias = NDArray[np.float64]
    # array_t: TypeAlias = NDArray[T]


# unique enough?
hash_block_type = Tuple[std.uint64_t, std.uint64_t, std.uint64_t, std.uint64_t]
parms_id_type = hash_block_type
