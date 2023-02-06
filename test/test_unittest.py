from pathlib import Path


class Test_Unittest:
    def test_unpack_list(self):
        ls = [10, 20]

        a, b = ls
        assert a == 10 and b == 20
