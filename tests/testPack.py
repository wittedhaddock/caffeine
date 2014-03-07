import unittest


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_listPack(self):
        import caffeine.pack
        lyst = [5, 4, 3]
        caffeine.pack.pack(lyst)

    def test_dictPack(self):
        import caffeine.pack
        dikt = {"base": "ball"}
        caffeine.pack.pack(dikt)
