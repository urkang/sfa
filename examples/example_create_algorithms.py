# -*- coding: utf-8 -*-

import sfa


if __name__ == "__main__":

    """
    algs = sfa.AlgorithmSet()
    algs.create("PW")
    algs.create("GS")
    algs.create("SP")

    The following code snippet is the same as the above.

    AlgorithmSet's create() without any argument creates all algorithms.
    """

    algs = sfa.AlgorithmSet()
    algs.create(["PW", "GS", "SP"])


    # Access with the id of algorithm
    alg_pw = algs["PW"]  # Pathway wiring
    alg_gs = algs["GS"]  # Gaussian smoothing
    alg_sp = algs["SP"]  # Signal propagation

    # Print the name of algorithm
    print(alg_pw.name)
    print(alg_gs.name)
    print(alg_sp.name)
       
    # Iterate Algorithms object
    for alg, obj in algs.items():
        print(alg, obj)




