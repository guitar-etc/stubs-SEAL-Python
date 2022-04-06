from typing import Tuple

import numpy as np

# VectorInt std::vector<std::int64_t>
# VectorDouble std::vector<double>

std_array = tuple
std_string = str
std_vector = list
std_size_t = int
std_uint64_t = np.uint64


# unique enough?
# using hash_block_type = std::array<std::uint64_t, hash_block_uint64_count>;
hash_block_type = Tuple[std_uint64_t, std_uint64_t, std_uint64_t, std_uint64_t]
# hash_block_type = std_array[std_uint64_t, std_uint64_t, std_uint64_t, std_uint64_t]
parms_id_type = hash_block_type
