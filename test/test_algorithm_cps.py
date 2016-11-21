# -*- coding: utf-8 -*-
import sys
if sys.version_info <= (2, 8):
    from builtins import super

import unittest

import numpy as np
import pandas as pd

import sfa
from sfa import calc_accuracy
from sfa import AlgorithmSet
from sfa import DataSet
from sfa.data import borisov_2009


class SimpleData(sfa.base.Data):
    def __init__(self):
        super().__init__()
        self._abbr = "SC"
        self._name = "Simple cascade"
        self._A = np.array([[0, 0, 0],
                            [1, 0, 0],
                            [0, 1, 0]], dtype=np.float)

        self._n2i = {"A": 0, "B": 1, "C": 2}
        self._df_ba = pd.DataFrame()
        self._df_exp = pd.DataFrame()

        self._dg = None  # nx.DiGraph()

class TestAlgorithmCPS(unittest.TestCase):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create an object for signal propagation algorithm
        self.algs = AlgorithmSet()
        self.algs.create("CPS")
        self.alg = self.algs["CPS"]

        # Create container for data.
        self.ds = DataSet()
        self.ds.create("NELANDER_2008")
        self.ds.create("BORISOV_2009")

        self.solutions = {}

        self.solutions["NELANDER_2008"] = 0.767

        self.solutions["BORISOV_2009_AUC_LOW"] = 0.692308
        self.solutions["BORISOV_2009_AUC_EGF"] = 0.704987
        self.solutions["BORISOV_2009_AUC_I"] = 0.788673
        self.solutions["BORISOV_2009_AUC_EGF+I"] = 0.772612

        self.solutions["BORISOV_2009_SS_LOW"] = 0.719358
        self.solutions["BORISOV_2009_SS_EGF"] = 0.654269
        self.solutions["BORISOV_2009_SS_I"] = 0.727811
        self.solutions["BORISOV_2009_SS_EGF+I"] = 0.662722
    # end of def __init__

    def test_simple_data_01(self):

        sdata = SimpleData()
        alg = self.alg
        alg.data = sdata
        alg.initialize()

        # Test #1
        alg.params.alpha = 0.5
        b = np.array([1.0, 0.0, 0.0])
        x = alg.compute(b)
        self.assertAlmostEqual(x[0], 1.0, 4)
        self.assertAlmostEqual(x[1], 0.5, 4)
        self.assertAlmostEqual(x[2], 0.25, 4)

        # Test #2
        alg.params.alpha = 0.9
        alg.initialize(data=False)
        b = np.array([1.0, 0.0, 0.0])
        x = alg.compute(b)
        self.assertAlmostEqual(x[0], 1.0, 4)
        self.assertAlmostEqual(x[1], 0.9, 4)
        self.assertAlmostEqual(x[2], 0.81, 4)

    def test_simple_data_02(self):

        sdata = SimpleData()

        sdata._A[1, 0] = -1
        sdata._A[2, 1] = -1

        alg = self.alg
        alg.data = sdata
        alg.initialize()

        # Test #1
        alg.params.alpha = 0.5
        b = np.array([1.0, 0.0, 0.0])
        x = alg.compute(b)
        self.assertAlmostEqual(x[0], 1.0, 4)
        self.assertAlmostEqual(x[1], -0.5, 4)
        self.assertAlmostEqual(x[2], 0.25, 4)

        # Test #2
        alg.params.alpha = 0.9
        alg.initialize(data=False)
        b = np.array([1.0, 0.0, 0.0])
        x = alg.compute(b)
        self.assertAlmostEqual(x[0], 1.0, 4)
        self.assertAlmostEqual(x[1], -0.9, 4)
        self.assertAlmostEqual(x[2], 0.81, 4)

    def test_simple_data_03(self):
        sdata = SimpleData()

        sdata._A[0, 2] = 1

        alg = self.alg
        alg.params.initialize()  # Use the default alpha value
        alg.data = sdata
        alg.initialize()
        b = np.array([1.0, 0.0, 0.0])
        x = alg.compute(b)

        self.assertAlmostEqual(x[0], 1.14285714, 4)
        self.assertAlmostEqual(x[1], 0.571428575, 4)
        self.assertAlmostEqual(x[2], 0.28571428, 4)


    def test_nelander(self):
        alg = self.alg
        data = self.ds["NELANDER_2008"]

        alg.params.initialize()
        alg.params.use_rel_change = True

        alg.data = data
        alg.initialize()
        alg.compute_batch()
        acc = calc_accuracy(alg.result.df_sim, data.df_exp)
        self.assertAlmostEqual(acc, self.solutions[data.abbr], 2)


    def test_borisov(self):
        alg = self.alg
        borisov = borisov_2009.create_test_data()
        alg.params.initialize()
        alg.params.use_rel_change = True
        alg.data = sfa.get_avalue(borisov)
        alg.initialize(data=False)
        for i, (abbr, data) in enumerate(borisov.items()):
            alg.data = data
            alg.initialize(network=False)

            alg.compute_batch()
            acc = calc_accuracy(alg.result.df_sim, data.df_exp)
            self.assertAlmostEqual(acc, self.solutions[abbr], 2)
        # end of for
    #end of def


if __name__ == "__main__":
    unittest.main(verbosity=2)