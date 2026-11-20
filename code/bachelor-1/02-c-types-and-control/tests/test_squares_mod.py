def test_square_roots_of_one_mod_256():
    assert [x for x in range(256) if x * x % 256 == 1] == [1, 127, 129, 255]
