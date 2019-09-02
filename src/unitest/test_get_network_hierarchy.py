import unittest
import pandas as pd
from src.functions.get_network_hierarchy import get_network_hierarchy
df = pd.read_csv(r'/home/yonathan/Python_projects/DataHack2019/data/draft/network_draft.csv')


class MyTestCase(unittest.TestCase):
    def test_get_network_hierarchy(self):
        df_hir = get_network_hierarchy(df)
        self.assertListEqual(list(df_hir.network_hierarchy), list(df_hir.real_hierarchy))


if __name__ == '__main__':
    unittest.main()
