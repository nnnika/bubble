import unittest
from bubble.data.api import DataApi

class DataApiTest(unittest.TestCase):

    da = DataApi()

    def test_get_factor(self):
        res = self.da.get_factor('factor_index_quote_close', '000001.SH', '2021-01-01', '2022-01-01')
        print(res)
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
