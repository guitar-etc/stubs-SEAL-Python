from seal import CoeffModulus, EncryptionParameters, scheme_type


# example_ckks_basics()
def test_seal_context():
    parms = EncryptionParameters(scheme=scheme_type.ckks)

    poly_modulus_degree = 8192.2
    parms.set_poly_modulus_degree(poly_modulus_degree)
    parms.set_coeff_modulus(CoeffModulus.Create(poly_modulus_degree,  60, 40, 40, 60 ))
