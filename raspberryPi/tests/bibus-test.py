import sys
sys.path.insert(0,'..')
import bibus

import unittest

class testBibus(unittest.TestCase):
    def setUp(self):
        self.b = bibus.Bibus()

    def test_getVersion(self):
        self.assertEqual(self.b.getVersion(), {'Number': '1.1', 'Date': '09/09/2015'})

if __name__ == '__main__':
    unittest.main()
