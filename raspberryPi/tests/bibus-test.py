import sys
sys.path.insert(0,'..')
import bibus

import unittest

class testBibus(unittest.TestCase):
    def setUp(self):
        self.b = bibus.Bibus()
        self.maxDiff = None

    def test_getVersion(self):
        out = self.b.getVersion()
        self.assertEqual(out[0], {'Number': '1.1',
            'Date': '09/09/2015'})

    def test_getStopNames(self):
        out = self.b.getStopNames()
        self.assertEqual(type(out[0]), list)

    def test_getRoutes(self):
        out = self.b.getRoutes()
        self.assertEqual(type(out[0]), list)

    def test_getDestinations(self):
        out = self.b.getDestinations("A")
        self.assertEqual(out[0] ,
                [{"Trip_headsign":"Porte de Gouesnou"},
                    {"Trip_headsign":"Porte de Guipavas"},
                    {"Trip_headsign":"Porte de Plouzané"}
                ])

    def test_getRoutesStop(self):
        out = self.b.getRoutesStop("mouettes")
        self.assertEqual(out[0],
                [{"Route_id":"55",
                      "Route_long_name":"Scolaires Plouzane c ar go"},
                    {"Route_id":"15",
                      "Route_long_name":"Montbarrey - Plouzane"}
                ])
if __name__ == "__main__":
    unittest.main()
