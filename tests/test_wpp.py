import unittest
import numpy as np
from pyvd.wpp import make_pop_dat, make_fert_dat

class TestWPP(unittest.TestCase):

    def test_make_pop_dat(self):
        pop_dat = make_pop_dat('IND')
        self.assertIsInstance(pop_dat, np.ndarray)
        self.assertEqual(pop_dat.shape[0], 22)  # Check number of rows
        self.assertGreater(pop_dat.shape[1], 0)  # Check there is at least one column

    def test_make_fert_dat(self):
        fert_dat = make_fert_dat('GHA')
        self.assertIsInstance(fert_dat, np.ndarray)
        self.assertEqual(fert_dat.shape[0], 21)  # Check number of rows
        self.assertGreater(fert_dat.shape[1], 0)  # Check there is at least one column

if __name__ == '__main__':
    unittest.main()
