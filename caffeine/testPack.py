import unittest


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_listPack(self):
        import pack
        lyst = [5, 4, 3]
        pack.pack(lyst)

    def test_dictPack(self):
        import pack
        dikt = {"base": "ball"}
        pack.pack(dikt)
