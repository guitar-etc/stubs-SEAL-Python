from stubs.cpp_types import double, std

from seal import (
    CKKSEncoder,
    CoeffModulus,
    Decryptor,
    EncryptionParameters,
    Encryptor,
    Evaluator,
    GaloisKeys,
    KeyGenerator,
    Plaintext,
    PublicKey,
    RelinKeys,
    SEALContext,
    scheme_type,
)

from .utils import LINE, print_line, print_parameters, print_vector


# example/5_ckks_basics.cpp
def test_seal_context():
    # In this example we demonstrate evaluating a polynomial function
    #     PI*x^3 + 0.4*x + 1
    # on encrypted floating-point input data x for a set of 4096 equidistant points
    # in the interval [0, 1]. This example demonstrates many of the main features
    # of the CKKS scheme, but also the challenges in using it.
    # We start by setting up the CKKS scheme.
    parms = EncryptionParameters(scheme_type.ckks)

    # We saw in `2_encoders.cpp' that multiplication in CKKS causes scales
    # in ciphertexts to grow. The scale of any ciphertext must not get too close
    # to the total size of coeff_modulus, or else the ciphertext simply runs out of
    # room to store the scaled-up plaintext. The CKKS scheme provides a `rescale'
    # functionality that can reduce the scale, and stabilize the scale expansion.
    # Rescaling is a kind of modulus switch operation (recall `3_levels.cpp').
    # As modulus switching, it removes the last of the primes from coeff_modulus,
    # but as a side-effect it scales down the ciphertext by the removed prime.
    # Usually we want to have perfect control over how the scales are changed,
    # which is why for the CKKS scheme it is more common to use carefully selected
    # primes for the coeff_modulus.
    # More precisely, suppose that the scale in a CKKS ciphertext is S, and the
    # last prime in the current coeff_modulus (for the ciphertext) is P. Rescaling
    # to the next level changes the scale to S/P, and removes the prime P from the
    # coeff_modulus, as usual in modulus switching. The number of primes limits
    # how many rescalings can be done, and thus limits the multiplicative depth of
    # the computation.
    # It is possible to choose the initial scale freely. One good strategy can be
    # to is to set the initial scale S and primes P_i in the coeff_modulus to be
    # very close to each other. If ciphertexts have scale S before multiplication,
    # they have scale S^2 after multiplication, and S^2/P_i after rescaling. If all
    # P_i are close to S, then S^2/P_i is close to S again. This way we stabilize the
    # scales to be close to S throughout the computation. Generally, for a circuit
    # of depth D, we need to rescale D times, i.e., we need to be able to remove D
    # primes from the coefficient modulus. Once we have only one prime left in the
    # coeff_modulus, the remaining prime must be larger than S by a few bits to
    # preserve the pre-decimal-point value of the plaintext.
    # Therefore, a generally good strategy is to choose parameters for the CKKS
    # scheme as follows:
    #     (1) Choose a 60-bit prime as the first prime in coeff_modulus. This will
    #         give the highest precision when decrypting;
    #     (2) Choose another 60-bit prime as the last element of coeff_modulus, as
    #         this will be used as the special prime and should be as large as the
    #         largest of the other primes;
    #     (3) Choose the intermediate primes to be close to each other.
    # We use CoeffModulus::Create to generate primes of the appropriate size. Note
    # that our coeff_modulus is 200 bits total, which is below the bound for our
    # poly_modulus_degree: CoeffModulus::MaxBitCount(8192) returns 218.
    poly_modulus_degree = 8192
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(
        CoeffModulus.Create(poly_modulus_degree, [60, 40, 40, 60])
    )

    # We choose the initial scale to be 2^40. At the last level, this leaves us
    # 60-40=20 bits of precision before the decimal point, and enough (roughly
    # 10-20 bits) of precision after the decimal point. Since our intermediate
    # primes are 40 bits (in fact, they are very close to 2^40), we can achieve
    # scale stabilization as described above.
    scale = pow(2.0, 40)
    context = SEALContext(parms)

    print_parameters(context)
    print()

    keygen = KeyGenerator(context)
    secret_key = keygen.secret_key()
    public_key = PublicKey()
    keygen.create_public_key(public_key)
    relin_keys = RelinKeys()
    keygen.create_relin_keys(relin_keys)
    gal_keys = GaloisKeys()
    keygen.create_galois_keys(gal_keys)
    encryptor = Encryptor(context, public_key)
    evaluator = Evaluator(context)
    decryptor = Decryptor(context, secret_key)

    encoder = CKKSEncoder(context)

    slot_count = encoder.slot_count()
    print(f"Number of slots: {slot_count}")

    input = [0.0] * slot_count

    curr_point = 0
    step_size = 1.0 / (slot_count - 1)
    for i in range(slot_count):
        input[i] = curr_point
        curr_point += step_size

    print(f"Input vector: ")
    print_vector(input, 3, 7)

    print("Evaluating polynomial PI*x^3 + 0.4x + 1 ...")

    # We create plaintexts for PI, 0.4, and 1 using an overload of CKKSEncoder::encode
    # that encodes the given floating-point value to every slot in the vector.
    plain_coeff3 = encoder.encode(3.14159265, scale)
    plain_coeff1 = encoder.encode(0.4, scale)
    plain_coeff0 = encoder.encode(1.0, scale)

    print_line(LINE())
    print("Encode input vectors.")
    x_plain = encoder.encode(input, scale)
    x1_encrypted = encryptor.encrypt(x_plain)

    # To compute x^3 we first compute x^2 and relinearize. However, the scale has
    # now grown to 2^80.
    print_line(LINE())
    print("Compute x^2 and relinearize:")
    x3_encrypted = evaluator.multiply(x1_encrypted, x1_encrypted)
    # x3_encrypted = evaluator.square(x1_encrypted);
    evaluator.relinearize_inplace(x3_encrypted, relin_keys)
    from math import log2

    print(
        f"    + Scale of x^2 before rescale: {log2(x3_encrypted.scale())} bits"
    )

    # Now rescale; in addition to a modulus switch, the scale is reduced down by
    # a factor equal to the prime that was switched away (40-bit prime). Hence, the
    # new scale should be close to 2^40. Note, however, that the scale is not equal
    # to 2^40: this is because the 40-bit prime is only close to 2^40.
    print_line(LINE())
    print("Rescale x^2.")
    evaluator.rescale_to_next_inplace(x3_encrypted)
    print(
        f"    + Scale of x^2 after rescale: {log2(x3_encrypted.scale())} bits"
    )

    # Now x3_encrypted is at a different level than x1_encrypted, which prevents us
    # from multiplying them to compute x^3. We could simply switch x1_encrypted to
    # the next parameters in the modulus switching chain. However, since we still
    # need to multiply the x^3 term with PI (plain_coeff3), we instead compute PI*x
    # first and multiply that with x^2 to obtain PI*x^3. To this end, we compute
    # PI*x and rescale it back from scale 2^80 to something close to 2^40.
    print_line(LINE())
    print("Compute and rescale PI*x.")
    x1_encrypted_coeff3 = evaluator.multiply_plain(x1_encrypted, plain_coeff3)
    print(
        f"    + Scale of PI*x before rescale: {log2(x1_encrypted_coeff3.scale())} bits"
    )
    evaluator.rescale_to_next_inplace(x1_encrypted_coeff3)
    print(
        f"    + Scale of PI*x after rescale: {log2(x1_encrypted_coeff3.scale())} bits"
    )

    # Since x3_encrypted and x1_encrypted_coeff3 have the same exact scale and use
    # the same encryption parameters, we can multiply them together. We write the
    # result to x3_encrypted, relinearize, and rescale. Note that again the scale
    # is something close to 2^40, but not exactly 2^40 due to yet another scaling
    # by a prime. We are down to the last level in the modulus switching chain.
    print_line(LINE())
    print("Compute, relinearize, and rescale (PI*x)*x^2.")
    evaluator.multiply_inplace(x3_encrypted, x1_encrypted_coeff3)
    evaluator.relinearize_inplace(x3_encrypted, relin_keys)
    print(
        f"    + Scale of PI*x^3 before rescale: {log2(x3_encrypted.scale())} bits"
    )
    evaluator.rescale_to_next_inplace(x3_encrypted)
    print(
        f"    + Scale of PI*x^3 after rescale: {log2(x3_encrypted.scale())} bits"
    )

    # Next we compute the degree one term. All this requires is one multiply_plain
    # with plain_coeff1. We overwrite x1_encrypted with the result.
    print_line(LINE())
    print("Compute and rescale 0.4*x.")
    evaluator.multiply_plain_inplace(x1_encrypted, plain_coeff1)
    print(
        f"    + Scale of 0.4*x before rescale: {log2(x1_encrypted.scale())} bits"
    )
    evaluator.rescale_to_next_inplace(x1_encrypted)
    print(
        f"    + Scale of 0.4*x after rescale: {log2(x1_encrypted.scale())} bits"
    )

    # Now we would hope to compute the sum of all three terms. However, there is
    # a serious problem: the encryption parameters used by all three terms are
    # different due to modulus switching from rescaling.
    # Encrypted addition and subtraction require that the scales of the inputs are
    # the same, and also that the encryption parameters (parms_id) match. If there
    # is a mismatch, Evaluator will throw an exception.
    # cout << endl;
    print_line(LINE())
    print("Parameters used by all three terms are different.")
    print(
        f"    + Modulus chain index for x3_enc) {context.get_context_data(x3_encrypted.parms_id()).chain_index()}"
    )
    print(
        f"    + Modulus chain index for x1_enc) {context.get_context_data(x1_encrypted.parms_id()).chain_index()}"
    )
    print(
        f"    + Modulus chain index for plain_) {context.get_context_data(plain_coeff0.parms_id()).chain_index()}"
    )

    # Let us carefully consider what the scales are at this point. We denote the
    # primes in coeff_modulus as P_0, P_1, P_2, P_3, in this order. P_3 is used as
    # the special modulus and is not involved in rescalings. After the computations
    # above the scales in ciphertexts are:
    #     - Product x^2 has scale 2^80 and is at level 2;
    #     - Product PI*x has scale 2^80 and is at level 2;
    #     - We rescaled both down to scale 2^80/P_2 and level 1;
    #     - Product PI*x^3 has scale (2^80/P_2)^2;
    #     - We rescaled it down to scale (2^80/P_2)^2/P_1 and level 0;
    #     - Product 0.4*x has scale 2^80;
    #     - We rescaled it down to scale 2^80/P_2 and level 1;
    #     - The contant term 1 has scale 2^40 and is at level 2.
    # Although the scales of all three terms are approximately 2^40, their exact
    # values are different, hence they cannot be added together.
    print_line(LINE())
    print("The exact scales of all three terms are different:")
    print(f"    + Exact scale in PI*x^3: {x3_encrypted.scale()}")
    print(f"    + Exact scale in  0.4*x: {x1_encrypted.scale()}")
    print(f"    + Exact scale in      1: {plain_coeff0.scale()}")

    # There are many ways to fix this problem. Since P_2 and P_1 are really close
    # to 2^40, we can simply "lie" to Microsoft SEAL and set the scales to be the
    # same. For example, changing the scale of PI*x^3 to 2^40 simply means that we
    # scale the value of PI*x^3 by 2^120/(P_2^2*P_1), which is very close to 1.
    # This should not result in any noticeable error.
    # Another option would be to encode 1 with scale 2^80/P_2, do a multiply_plain
    # with 0.4*x, and finally rescale. In this case we would need to additionally
    # make sure to encode 1 with appropriate encryption parameters (parms_id).
    # In this example we will use the first (simplest) approach and simply change
    # the scale of PI*x^3 and 0.4*x to 2^40.
    print_line(LINE())
    print("Normalize scales to 2^40.")
    x3_encrypted.scale(pow(2.0, 40))
    x1_encrypted.scale(pow(2.0, 40))

    # We still have a problem with mismatching encryption parameters. This is easy
    # to fix by using traditional modulus switching (no rescaling). CKKS supports
    # modulus switching just like the BFV scheme, allowing us to switch away parts
    # of the coefficient modulus when it is simply not needed.
    print_line(LINE())
    print("Normalize encryption parameters to the lowest level.")
    last_parms_id = x3_encrypted.parms_id()
    evaluator.mod_switch_to_inplace(x1_encrypted, last_parms_id)
    evaluator.mod_switch_to_inplace(plain_coeff0, last_parms_id)

    # All three ciphertexts are now compatible and can be added.
    print_line(LINE())
    print("Compute PI*x^3 + 0.4*x + 1.")
    encrypted_result = evaluator.add(x3_encrypted, x1_encrypted)
    evaluator.add_plain_inplace(encrypted_result, plain_coeff0)

    # First print the true result.
    plain_result: Plaintext
    print_line(LINE())
    print("Decrypt and decode PI*x^3 + 0.4x + 1.")
    print("    + Expected result:")
    true_result: std.vector[double] = []
    for x in input:
        true_result.append((3.14159265 * x * x + 0.4) * x + 1)

    print_vector(true_result, 3, 7)

    # Decrypt, decode, and print the result.
    plain_result = decryptor.decrypt(encrypted_result)
    result = encoder.decode(plain_result)
    print("    + Computed result ...... Correct.")
    print_vector(result, 3, 7)

    # While we did not show any computations on complex numbers in these examples,
    # the CKKSEncoder would allow us to have done that just as easily. Additions
    # and multiplications of complex numbers behave just as one would expect.

    from numpy.testing import assert_almost_equal

    assert_almost_equal(result[:3], true_result[:3], decimal=7)
