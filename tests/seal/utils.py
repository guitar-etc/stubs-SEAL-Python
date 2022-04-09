import sys

from stubs.cpp_types import T, np, std

from seal import SEALContext, scheme_type

# imported from cpp_types
# T = TypeVar("T")


def LINE():
    return sys._getframe(1).f_lineno  # type: ignore


# Helper function: Print line number.
def print_line(line_number: int):
    print(f"Line {line_number} --> ")
    # TODO setw
    # std::cout << "Line " << std::setw(3) << line_number << " --> ";


def print_vector(vector: std.vector[T], size: int, precision: int):
    with np.printoptions(precision=precision):
        print(np.array(vector[:size]))  # type: ignore


# from seal import CoeffModulus, EncryptionParameters, SEALContext, scheme_type
# Helper function: Prints the parameters in a SEALContext.
def print_parameters(context: SEALContext):
    context_data = context.key_context_data()

    cd_parms = context_data.parms()
    # Which scheme are we using?
    scheme_name = context_data.parms().scheme().name.upper()

    texts: list[str] = []
    texts.append(
        f"""/
| Encryption parameters:
|   scheme: {scheme_name}
|   poly_modulus_degree: {context_data.parms().poly_modulus_degree()}
"""
    )

    # Print the size of the true (product) coefficient modulus.
    coeff_modulus = context_data.parms().coeff_modulus()
    texts.append(
        f"|   coeff_modulus_size: {context_data.total_coeff_modulus_bit_count()} ("
    )
    for coeff_modulo in coeff_modulus:
        texts.append(f"{coeff_modulo.bit_count()} + ")
    texts.append(f"{coeff_modulus[-1].bit_count()} ) bits\n")

    # For the BFV scheme print the plain_modulus parameter.
    if cd_parms.scheme() == scheme_type.bfv:
        texts.append(
            f"|   plain_modulus: {cd_parms.plain_modulus().value()}\n"
        )
    texts.append("\\\n")

    print("".join(texts))
