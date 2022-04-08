from typing import Tuple, TypeAlias

import numpy as np
from numpy.typing import NDArray

# VectorInt std::vector<std::int64_t>
# VectorDouble std::vector<double>

double = float
long = int
int = int
bool = bool


class py:
    array_t: TypeAlias = NDArray


class std:
    array: TypeAlias = tuple
    string: TypeAlias = str
    vector: TypeAlias = list
    size_t: TypeAlias = int
    uint64_t: TypeAlias = np.uint64
    streamoff: TypeAlias = long


# unique enough?
hash_block_type = Tuple[std.uint64_t, std.uint64_t, std.uint64_t, std.uint64_t]
parms_id_type = hash_block_type
