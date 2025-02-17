import unittest
import numpy as np
from pyvd.base import demog_vd_calc
from pyvd.wpp import make_pop_dat
import pyvd.constants

class TestBase(unittest.TestCase):

    def test_demog_vd_calc(self):
        pop_input = make_pop_dat('IND')
        year_vec = pop_input[0, :] - pyvd.constants.BASE_YEAR
        year_init = pyvd.constants.BASE_YEAR - pyvd.constants.BASE_YEAR
        pop_mat = pop_input[1:, :] + 0.1
        vd_tup = demog_vd_calc(year_vec, year_init, pop_mat)
        
        self.assertEqual(len(vd_tup), 6)
        self.assertIsInstance(vd_tup[0], list)  # mort_year
        self.assertIsInstance(vd_tup[1], np.ndarray)  # mort_mat
        self.assertIsInstance(vd_tup[3], float)  # birth_rate
        self.assertIsInstance(vd_tup[4], np.ndarray)  # brmultx_02
        self.assertIsInstance(vd_tup[5], np.ndarray)  # brmulty_02

if __name__ == '__main__':
    unittest.main()
