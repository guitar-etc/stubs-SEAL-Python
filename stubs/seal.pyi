from typing import Any, ClassVar, List, overload

import numpy as np
from numpy.typing import NDArray

from stubs.cpp_types import bool, double, int, parms_id_type, py, std

class BatchEncoder:
    def __init__(self, arg0: SEALContext) -> None: ...
    def decode(self, arg0: Plaintext) -> NDArray[np.int64]: ...
    def encode(self, arg0: NDArray[np.int64]) -> Plaintext: ...
    def slot_count(self) -> int: ...

class CKKSEncoder:
    def __init__(self, context: SEALContext) -> None: ...
    def decode(self, plain: Plaintext) -> py.array_t_double: ...
    @overload
    def encode(
        self, values: py.array_t_double, scale: double
    ) -> Plaintext: ...
    @overload
    def encode(self, arg0: double, arg1: double) -> Plaintext: ...
    def slot_count(self) -> std.size_t: ...

class Ciphertext:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, context: SEALContext) -> None: ...
    @overload
    def __init__(
        self, context: SEALContext, parms_id: parms_id_type
    ) -> None: ...
    @overload
    def __init__(
        self, arg0: SEALContext, arg1: parms_id_type, size_capacity: std.size_t
    ) -> None: ...
    @overload
    def __init__(self, other: Ciphertext) -> None: ...
    def coeff_modulus_size(self) -> std.size_t: ...
    def poly_modulus_degree(self) -> std.size_t: ...
    def size(self) -> std.size_t: ...
    def size_capacity(self) -> std.size_t: ...
    def is_transparent(self) -> bool: ...
    def is_ntt_form(self) -> bool: ...
    def parms_id(self) -> parms_id_type: ...
    @overload
    def scale(self) -> double: ...
    @overload
    def scale(self, scale: double) -> None: ...
    def save(self, path: std.string) -> None: ...
    def load(self, contet: SEALContext, path: std.string) -> None: ...
    def save_size(self) -> std.streamoff: ...

class CoeffModulus:
    @classmethod
    def MaxBitCount(
        cls,
        poly_modulus_degree: std.size_t,
        sec_level: sec_level_type = ...,
        # sec_level: sec_level_type = sec_level_type.tc128,
    ) -> Any: ...
    @classmethod
    def BFVDefault(
        cls,
        poly_modulus_degree: std.size_t,
        sec_level: sec_level_type = ...,
        # sec_level: sec_level_type = sec_level_type.tc128,
    ) -> Any: ...
    @classmethod
    def Create(
        cls, poly_modulus_degree: std.size_t, bit_sizes: std.vector[int]
    ) -> Any: ...

class ContextData:
    def __init__(self, *args, **kwargs) -> None: ...
    def chain_index(self) -> int: ...
    def next_context_data(self) -> ContextData: ...
    def parms(self) -> EncryptionParameters: ...
    def parms_id(self) -> parms_id_type: ...
    def qualifiers(self) -> EncryptionParameterQualifiers: ...
    def total_coeff_modulus(self) -> int: ...
    def total_coeff_modulus_bit_count(self) -> int: ...

class Decryptor:
    def __init__(self, arg0: SEALContext, arg1: SecretKey) -> None: ...
    @overload
    def decrypt(self, arg0: Ciphertext, arg1: Plaintext) -> None: ...
    @overload
    def decrypt(self, arg0: Ciphertext) -> Plaintext: ...
    def invariant_noise_budget(self, arg0: Ciphertext) -> int: ...

class EncryptionParameterQualifiers:
    sec_level: sec_level_type
    using_batching: bool
    using_descending_modulus_chain: bool
    using_fast_plain_lift: bool
    using_fft: bool
    using_ntt: bool
    def __init__(self, *args, **kwargs) -> None: ...
    def parameters_set(self) -> bool: ...

class EncryptionParameters:
    @overload
    def __init__(self, scheme: scheme_type) -> None: ...
    @overload
    def __init__(self, copy: EncryptionParameters) -> None: ...
    def set_poly_modulus_degree(self, arg: std.size_t) -> None: ...
    def set_coeff_modulus(self, arg: std.vector[Modulus]) -> None: ...
    @overload
    def set_plain_modulus(self, arg: Modulus) -> None: ...
    @overload
    def set_plain_modulus(self, arg: std.uint64_t) -> None: ...
    def scheme(self) -> scheme_type: ...
    def poly_modulus_degree(self) -> std.size_t: ...
    def coeff_modulus(self) -> std.vector[Modulus]: ...
    def plain_modulus(self) -> Modulus: ...
    def save(self, path: std.string) -> None: ...
    def load(self, path: std.string) -> None: ...
    def __getstate__(self) -> tuple[std.string]: ...
    def __setstate__(self, t: tuple[std.string]) -> None: ...

class Encryptor:
    @overload
    def __init__(self, arg0: SEALContext, arg1: PublicKey) -> None: ...
    @overload
    def __init__(self, arg0: SEALContext, arg1: SecretKey) -> None: ...
    @overload
    def __init__(
        self, arg0: SEALContext, arg1: PublicKey, arg2: SecretKey
    ) -> None: ...
    def encrypt(self, arg0: Plaintext) -> Ciphertext: ...
    def encrypt_zero(self) -> Ciphertext: ...
    def set_public_key(self, arg0: PublicKey) -> None: ...
    def set_secret_key(self, arg0: SecretKey) -> None: ...

class Evaluator:
    def __init__(self, arg0: SEALContext) -> None: ...
    def add(self, arg0: Ciphertext, arg1: Ciphertext) -> Ciphertext: ...
    def add_inplace(self, arg0: Ciphertext, arg1: Ciphertext) -> None: ...
    def add_many(self, arg0: List[Ciphertext]) -> Ciphertext: ...
    def add_plain(self, arg0: Ciphertext, arg1: Plaintext) -> Ciphertext: ...
    def add_plain_inplace(self, arg0: Ciphertext, arg1: Plaintext) -> None: ...
    def apply_galois(
        self, arg0: Ciphertext, arg1: int, arg2: GaloisKeys
    ) -> Ciphertext: ...
    def apply_galois_inplace(
        self, arg0: Ciphertext, arg1: int, arg2: GaloisKeys
    ) -> None: ...
    def complex_conjugate(
        self, arg0: Ciphertext, arg1: GaloisKeys
    ) -> Ciphertext: ...
    def complex_conjugate_inplace(
        self, arg0: Ciphertext, arg1: GaloisKeys
    ) -> None: ...
    def exponentiate(
        self, arg0: Ciphertext, arg1: int, arg2: RelinKeys
    ) -> Ciphertext: ...
    def exponentiate_inplace(
        self, arg0: Ciphertext, arg1: int, arg2: RelinKeys
    ) -> None: ...
    @overload
    def mod_switch_to(
        self, arg0: Ciphertext, arg1: parms_id_type
    ) -> Ciphertext: ...
    @overload
    def mod_switch_to(
        self, arg0: Plaintext, arg1: parms_id_type
    ) -> Plaintext: ...
    @overload
    def mod_switch_to_inplace(
        self, arg0: Ciphertext, arg1: parms_id_type
    ) -> None: ...
    @overload
    def mod_switch_to_inplace(
        self, arg0: Plaintext, arg1: parms_id_type
    ) -> None: ...
    @overload
    def mod_switch_to_next(self, arg0: Ciphertext) -> Ciphertext: ...
    @overload
    def mod_switch_to_next(self, arg0: Plaintext) -> Plaintext: ...
    @overload
    def mod_switch_to_next_inplace(self, arg0: Ciphertext) -> None: ...
    @overload
    def mod_switch_to_next_inplace(self, arg0: Plaintext) -> None: ...
    def multiply(self, arg0: Ciphertext, arg1: Ciphertext) -> Ciphertext: ...
    def multiply_inplace(self, arg0: Ciphertext, arg1: Ciphertext) -> None: ...
    def multiply_many(
        self, arg0: List[Ciphertext], arg1: RelinKeys
    ) -> Ciphertext: ...
    def multiply_plain(
        self, arg0: Ciphertext, arg1: Plaintext
    ) -> Ciphertext: ...
    def multiply_plain_inplace(
        self, arg0: Ciphertext, arg1: Plaintext
    ) -> None: ...
    def negate(self, arg0: Ciphertext) -> Ciphertext: ...
    def negate_inplace(self, arg0: Ciphertext) -> None: ...
    def relinearize(self, arg0: Ciphertext, arg1: RelinKeys) -> Ciphertext: ...
    def relinearize_inplace(
        self, arg0: Ciphertext, arg1: RelinKeys
    ) -> None: ...
    def rescale_to(
        self, arg0: Ciphertext, arg1: parms_id_type
    ) -> Ciphertext: ...
    def rescale_to_inplace(
        self, arg0: Ciphertext, arg1: parms_id_type
    ) -> None: ...
    def rescale_to_next(self, arg0: Ciphertext) -> Ciphertext: ...
    def rescale_to_next_inplace(self, arg0: Ciphertext) -> None: ...
    def rotate_columns(
        self, arg0: Ciphertext, arg1: GaloisKeys
    ) -> Ciphertext: ...
    def rotate_columns_inplace(
        self, arg0: Ciphertext, arg1: GaloisKeys
    ) -> None: ...
    def rotate_rows(
        self, arg0: Ciphertext, arg1: int, arg2: GaloisKeys
    ) -> Ciphertext: ...
    def rotate_rows_inplace(
        self, arg0: Ciphertext, arg1: int, arg2: GaloisKeys
    ) -> None: ...
    def rotate_vector(
        self, arg0: Ciphertext, arg1: int, arg2: GaloisKeys
    ) -> Ciphertext: ...
    def rotate_vector_inplace(
        self, arg0: Ciphertext, arg1: int, arg2: GaloisKeys
    ) -> None: ...
    def square(self, arg0: Ciphertext) -> Ciphertext: ...
    def square_inplace(self, arg0: Ciphertext) -> None: ...
    def sub(self, arg0: Ciphertext, arg1: Ciphertext) -> Ciphertext: ...
    def sub_inplace(self, arg0: Ciphertext, arg1: Ciphertext) -> None: ...
    def sub_plain(self, arg0: Ciphertext, arg1: Plaintext) -> Ciphertext: ...
    def sub_plain_inplace(self, arg0: Ciphertext, arg1: Plaintext) -> None: ...
    def transform_from_ntt(self, arg0: Ciphertext) -> Ciphertext: ...
    def transform_from_ntt_inplace(self, arg0: Ciphertext) -> None: ...
    @overload
    def transform_to_ntt(
        self, arg0: Plaintext, arg1: parms_id_type
    ) -> Plaintext: ...
    @overload
    def transform_to_ntt(self, arg0: Ciphertext) -> Ciphertext: ...
    @overload
    def transform_to_ntt_inplace(
        self, arg0: Plaintext, arg1: parms_id_type
    ) -> None: ...
    @overload
    def transform_to_ntt_inplace(self, arg0: Ciphertext) -> None: ...

class GaloisKeys(KSwitchKeys):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: KSwitchKeys) -> None: ...
    def get_index(self, *args, **kwargs) -> Any: ...
    def has_key(self, arg0: int) -> bool: ...
    def load(self, arg0: SEALContext, arg1: std.string) -> None: ...
    def parms_id(self) -> parms_id_type: ...
    def save(self, arg0: std.string) -> None: ...
    def size(self) -> int: ...

class KSwitchKeys:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: KSwitchKeys) -> None: ...
    def load(self, arg0: SEALContext, arg1: std.string) -> None: ...
    def parms_id(self) -> parms_id_type: ...
    def save(self, arg0: std.string) -> None: ...
    def size(self) -> int: ...

class KeyGenerator:
    @overload
    def __init__(self, context: SEALContext) -> None: ...
    @overload
    def __init__(
        self, context: SEALContext, secret_key: SecretKey
    ) -> None: ...
    def secret_key(self) -> SecretKey: ...
    @overload
    def create_public_key(self, pk: PublicKey) -> None: ...
    @overload
    def create_public_key(self) -> PublicKey: ...
    @overload
    def create_relin_keys(self, rk: RelinKeys) -> None: ...
    @overload
    def create_relin_keys(self) -> RelinKeys: ...
    @overload
    def create_galois_keys(
        self, arg0: std.vector[int], gk: GaloisKeys
    ) -> None: ...
    @overload
    def create_galois_keys(self, gk: GaloisKeys) -> None: ...
    @overload
    def create_galois_keys(self) -> GaloisKeys: ...

class Modulus:
    def __init__(self, arg0: int) -> None: ...
    def bit_count(self) -> int: ...
    def is_prime(self) -> bool: ...
    def is_zero(self) -> bool: ...
    def value(self) -> int: ...

class PlainModulus:
    def __init__(self, *args, **kwargs) -> None: ...
    def Batching(self, *args, **kwargs) -> Any: ...

class Plaintext:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: int | std.string | Plaintext) -> None: ...
    @overload
    def __init__(self, arg0: int, arg1: int) -> None: ...
    def capacity(self) -> int: ...
    def coeff_count(self) -> int: ...
    def is_ntt_form(self) -> bool: ...
    def is_zero(self) -> bool: ...
    def load(self, arg0: SEALContext, arg1: std.string) -> None: ...
    def nonzero_coeff_count(self) -> int: ...
    def parms_id(self) -> parms_id_type: ...
    def save(self, arg0: std.string) -> None: ...
    def save_size(self) -> int: ...
    @overload
    def scale(self) -> float: ...
    @overload
    def scale(self, arg0: float) -> None: ...
    @overload
    def set_zero(self, arg0: int, arg1: int) -> None: ...
    @overload
    def set_zero(self, arg0: int) -> None: ...
    @overload
    def set_zero(self) -> None: ...
    def significant_coeff_count(self) -> int: ...
    def to_string(self) -> std.string: ...

class PublicKey:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, copy: PublicKey) -> None: ...
    def parms_id(self) -> parms_id_type: ...
    def save(self, path: std.string) -> None: ...
    def load(self, context: SEALContext, path: std.string) -> None: ...

class RelinKeys(KSwitchKeys):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg0: KSwitchKeys) -> None: ...
    def get_index(self, *args, **kwargs) -> Any: ...
    def has_key(self, arg0: int) -> bool: ...
    def load(self, arg0: SEALContext, arg1: std.string) -> None: ...
    def parms_id(self) -> parms_id_type: ...
    def save(self, arg0: std.string) -> None: ...
    def size(self) -> int: ...

class SEALContext:
    def __init__(
        self,
        parms: EncryptionParameters,
        expand_mod_chain: bool = ...,
        # expand_mod_chain: bool = True,
        sec_level: sec_level_type = ...,
        # sec_level: sec_level_type = sec_level_type.tc128,
    ) -> None: ...
    def get_context_data(self, parms_id: parms_id_type) -> ContextData: ...
    def key_context_data(self) -> ContextData: ...
    def first_context_data(self) -> ContextData: ...
    def last_context_data(self) -> ContextData: ...
    def parameters_set(self) -> bool: ...
    def first_parms_id(self) -> parms_id_type: ...
    def last_parms_id(self) -> parms_id_type: ...
    def using_keyswitching(self) -> bool: ...

class SecretKey:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, copy: SecretKey) -> None: ...
    def parms_id(self) -> parms_id_type: ...
    def save(self, path: std.string) -> None: ...
    def load(self, context: SEALContext, path: std.string) -> None: ...

# class VectorDouble:
#     __hash__: ClassVar[None] = ...
#     @overload
#     def __init__(self, arg0: buffer) -> None: ...
#     @overload
#     def __init__(self) -> None: ...
#     @overload
#     def __init__(self, arg0: VectorDouble) -> None: ...
#     @overload
#     def __init__(self, arg0: Iterable) -> None: ...
#     def append(self, x: float) -> None: ...
#     def clear(self) -> None: ...
#     def count(self, x: float) -> int: ...
#     @overload
#     def extend(self, L: VectorDouble) -> None: ...
#     @overload
#     def extend(self, L: Iterable) -> None: ...
#     def insert(self, i: int, x: float) -> None: ...
#     @overload
#     def pop(self) -> float: ...
#     @overload
#     def pop(self, i: int) -> float: ...
#     def remove(self, x: float) -> None: ...
#     def __bool__(self) -> bool: ...
#     def __contains__(self, x: float) -> bool: ...
#     @overload
#     def __delitem__(self, arg0: int) -> None: ...
#     @overload
#     def __delitem__(self, arg0: slice) -> None: ...
#     def __eq__(self, arg0: VectorDouble) -> bool: ...
#     @overload
#     def __getitem__(self, s: slice) -> VectorDouble: ...
#     @overload
#     def __getitem__(self, arg0: int) -> float: ...
#     def __iter__(self) -> Iterator: ...
#     def __len__(self) -> int: ...
#     def __ne__(self, arg0: VectorDouble) -> bool: ...
#     @overload
#     def __setitem__(self, arg0: int, arg1: float) -> None: ...
#     @overload
#     def __setitem__(self, arg0: slice, arg1: VectorDouble) -> None: ...

# class VectorInt:
#     __hash__: ClassVar[None] = ...
#     @overload
#     def __init__(self, arg0: buffer) -> None: ...
#     @overload
#     def __init__(self) -> None: ...
#     @overload
#     def __init__(self, arg0: VectorInt) -> None: ...
#     @overload
#     def __init__(self, arg0: Iterable) -> None: ...
#     def append(self, x: int) -> None: ...
#     def clear(self) -> None: ...
#     def count(self, x: int) -> int: ...
#     @overload
#     def extend(self, L: VectorInt) -> None: ...
#     @overload
#     def extend(self, L: Iterable) -> None: ...
#     def insert(self, i: int, x: int) -> None: ...
#     @overload
#     def pop(self) -> int: ...
#     @overload
#     def pop(self, i: int) -> int: ...
#     def remove(self, x: int) -> None: ...
#     def __bool__(self) -> bool: ...
#     def __contains__(self, x: int) -> bool: ...
#     @overload
#     def __delitem__(self, arg0: int) -> None: ...
#     @overload
#     def __delitem__(self, arg0: slice) -> None: ...
#     def __eq__(self, arg0: VectorInt) -> bool: ...
#     @overload
#     def __getitem__(self, s: slice) -> VectorInt: ...
#     @overload
#     def __getitem__(self, arg0: int) -> int: ...
#     def __iter__(self) -> Iterator: ...
#     def __len__(self) -> int: ...
#     def __ne__(self, arg0: VectorInt) -> bool: ...
#     @overload
#     def __setitem__(self, arg0: int, arg1: int) -> None: ...
#     @overload
#     def __setitem__(self, arg0: slice, arg1: VectorInt) -> None: ...

# TODO change to python enum?
class error_type:
    # __doc__: ClassVar[std.string] = ...  # read-only
    __members__: ClassVar[dict] = ...  # read-only
    __entries: ClassVar[dict] = ...
    failed_creating_rns_base: ClassVar[error_type] = ...
    failed_creating_rns_tool: ClassVar[error_type] = ...
    invalid_coeff_modulus_bit_count: ClassVar[error_type] = ...
    invalid_coeff_modulus_no_ntt: ClassVar[error_type] = ...
    invalid_coeff_modulus_size: ClassVar[error_type] = ...
    invalid_parameters_insecure: ClassVar[error_type] = ...
    invalid_parameters_too_large: ClassVar[error_type] = ...
    invalid_plain_modulus_bit_count: ClassVar[error_type] = ...
    invalid_plain_modulus_coprimality: ClassVar[error_type] = ...
    invalid_plain_modulus_nonzero: ClassVar[error_type] = ...
    invalid_plain_modulus_too_large: ClassVar[error_type] = ...
    invalid_poly_modulus_degree: ClassVar[error_type] = ...
    invalid_poly_modulus_degree_non_power_of_two: ClassVar[error_type] = ...
    invalid_scheme: ClassVar[error_type] = ...
    none: ClassVar[error_type] = ...
    success: ClassVar[error_type] = ...
    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> std.string: ...
    @property
    def value(self) -> int: ...

# TODO change to python enum?
class scheme_type:
    # __doc__: ClassVar[std.string] = ...  # read-only
    __members__: ClassVar[dict] = ...  # read-only
    __entries: ClassVar[dict] = ...
    bfv: ClassVar[scheme_type] = ...
    ckks: ClassVar[scheme_type] = ...
    none: ClassVar[scheme_type] = ...
    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> std.string: ...
    @property
    def value(self) -> int: ...

# TODO change to python enum?
class sec_level_type:
    # __doc__: ClassVar[std.string] = ...  # read-only
    __members__: ClassVar[dict] = ...  # read-only
    __entries: ClassVar[dict] = ...
    none: ClassVar[sec_level_type] = ...
    tc128: ClassVar[sec_level_type] = ...
    tc192: ClassVar[sec_level_type] = ...
    tc256: ClassVar[sec_level_type] = ...
    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> std.string: ...
    @property
    def value(self) -> int: ...
