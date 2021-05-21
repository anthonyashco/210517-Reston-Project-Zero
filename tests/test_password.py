from security.password import Password as p


def test_salt():
    """Generate 100 salts and ensure none are repeating."""
    salts = []
    try:
        for _ in range(100):
            salts.append(p.salt_shaker())
        for i, salt in enumerate(salts):
            for j in range(i + 1, len(salts)):
                assert salt != salts[j]
    except ImportError:
        return False


def test_generate_password():
    griddle = p.hash_griddle("potato")
    assert p.check_pass("potato", griddle[0], griddle[1])
    assert not p.check_pass("potahto", griddle[0], griddle[1])


def test_saved_password():
    pass_hash = (
        "de408fec2ba4acf7a29f01798df5d4a12f0d73bda4ab49b91d602b62a7baf5c3" +
        "90100c025e93d4d380e320c5d24b06574d5c2ec4e3eea95f4eb9b04a7a113e26" +
        "eef3fd4f731495e5009ae76048baf1e6db2c9e1d70108479ab601feb2c2acdd2" +
        "4046d553e9be1c37a191af72895fbfe739b3d6699fba57d72af9f28cddcfd19c")
    pass_salt = 'd7c7371d702b005c48be283b5357c756'
    assert p.check_pass("potato", pass_hash, pass_salt)
    assert not p.check_pass("potahto", pass_hash, pass_salt)
