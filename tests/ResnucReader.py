import unittest
from reader.ResnucReader import ResnucReader as RR
import utils.PhysicsQuantities as PQ


class TestResnucReader(unittest.TestCase):
    def setUp(self):
        self.reader = RR()
        self.maxDiff = None

    def testTabLisRead(self):
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc= 0.99*2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc= 0.001845*2.2300E+10)]}}
        data = self.reader.load("ResnucInputTest_tab.lis")
        self.assertItemsEqual(data, res)

    @unittest.skip("To be implemented")
    def testTabLisReadMultiDet(self):
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc= 0.99*2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc= 0.001845*2.2300E+10)]},
               "": {"Isotope": [PQ.Isotope(75, 32, 0),
                                PQ.Isotope(26, 13, 1)],
                    "Activity": [PQ.Activity(2.0663E+05, unc= 0.99*2.0663E+05),
                                PQ.Activity(2.2300E+10, unc= 0.001845*2.2300E+10)]}}
        data = self.reader.load("ResnucInputTestMultiDet_tab.lis")
        self.assertItemsEqual(data, res)


    @unittest.skip("To be implemented")
    def testMultiFileReadSingleDet(self):
        data = self.reader.load(["ResnucInputTest_tab.lis", "ResnucInputTest2_tab.lis"])
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc= 0.99*2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc= 0.001845*2.2300E+10)]}}
        self.assertFalse(True, "To be implemented")

    @unittest.skip("To be implemented")
    def testMultiFileReadMultiDet(self):
        data = self.reader.load(["ResnucInputTest_tab.lis", "ResnucInputTest2_tab.lis"])
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc= 0.99*2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc= 0.001845*2.2300E+10)]}}
        self.assertFalse(True, "To be implemented")

    @unittest.skip("To be implemented")
    def testMultiFileReadWeighted(self):
        data = self.reader.load(["ResnucInputTest_tab.lis", "ResnucInputTest2_tab.lis"])
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc= 0.99*2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc= 0.001845*2.2300E+10)]}}
        self.assertFalse(True, )

    @unittest.skip("To be implemented")
    def testMultiFileReadMultiDetWeighted(self):
        data = self.reader.load(["ResnucInputTest_tab.lis", "ResnucInputTest2_tab.lis"])
        res = {"AlBa-1s": {"Isotope": [PQ.Isotope(75, 32, 0),
                                       PQ.Isotope(26, 13, 1)],
                           "Activity": [PQ.Activity(2.0663E+05, unc= 0.99*2.0663E+05),
                                        PQ.Activity(2.2300E+10, unc= 0.001845*2.2300E+10)]}}
        self.assertFalse(True, "To be implemented")