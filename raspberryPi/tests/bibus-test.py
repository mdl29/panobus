import sys
sys.path.insert(0,'..')
import bibus

import unittest

class testBibus(unittest.TestCase):
    def setUp(self):
        self.b = bibus.Bibus()
        self.maxDiff = None
        
    def test_getUri(self):
        # TODO add more tests, with multiple parameters, spaces ...
        self.assertEqual(self.b.getUri("getVersion"), "/WIPOD01/Transport/REST/getVersion?format=json")

    def test_getVersion(self):
        out = self.b.getVersion()
        #print("\n",out)
        self.assertEqual(out[0], {'Number': '1.1',
            'Date': '09/09/2015'})

    def test_getStopNames(self):
        out = self.b.getStopNames()
        #print("\n",out)
        self.assertEqual(type(out[0]), list)

    def test_getRoutes(self):
        out = self.b.getRoutes()
        #print("\n",out)
        self.assertEqual(type(out[0]), list)

    def test_getDestinations(self):
        out = self.b.getDestinations("A")
        #print("\n",out)
        self.assertEqual(out[0] ,
                [{"Trip_headsign":"Porte de Gouesnou"},
                    {"Trip_headsign":"Porte de Guipavas"},
                    {"Trip_headsign":"Porte de Plouzané"}
                ])

    def test_getRoutesStop(self):
        out = self.b.getRoutesStop("mouettes")
        #print("\n",out)
        self.assertEqual(out[0],
                [{"Route_id":"55",
                      "Route_long_name":"Scolaires Plouzane c ar go"},
                    {"Route_id":"15",
                      "Route_long_name":"Montbarrey - Plouzane"}
                ])
                
    def test_getStopVehiclesPosition(self):
        out = self.b.getStopVehiclesPosition("15","montbarrey")
        #print("\n",out)
    
    def test_getStop(self):
        stopName = "8 mai 1945"
        out = self.b.getStop( stopName )
        self.assertEqual(out[0][0]["Stop_name"], stopName)
    
    def test_getRemainingTimes(self):
        out = self.b.getRemainingTimes("A","liberte","porte de gouesnou")
        print("\n",out)
        self.assertEqual(type(out[0][0]["Advance"]),str)
    
if __name__ == "__main__":
    unittest.main()
