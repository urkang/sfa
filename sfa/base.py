
from abc import ABC, abstractmethod


class Result(ABC):
    pass

# end of class Result


class ContainerItem(ABC):
    def __init__(self, abbr=None, name=None):
        """
        abbr: Abbreviation (or symbol) representing this item
        name: Full name of this item
        """
        self._abbr = abbr
        self._name = name

    def __str__(self):
        return self._abbr

    def __repr__(self):
        class_name = self.__class__.__name__
        return "%s object" % (class_name)

    # Read-only properties
    @property
    def abbr(self):
        return self._abbr

    @property
    def name(self):
        return self._name


class Algorithm(ContainerItem):
    """
    The algorithms should implement compute method.    
    
    Usage:
        >>> class AnAlgorithm(sfa.Algorithm):
                ...
                ...        
        
        >>> alg = AnAlgorithm()
        >>> alg.params = params_obj # Parameters of the algorithm
        >>> alg.data = data_obj # Data to be analyzed by the algorithm
        >>> alg.initialize()
        >>> res = alg.compute()    
        
    """
    def __init__(self, abbr):
        """
        abbr: Abbreviation of algorithm name
        name: Full name of this algorithm
        """
        super().__init__(abbr)
        self._data = None
        self._params = None
        self._result = None

    # Read-only properties
    @property
    def result(self):
        return self._result

    # Read & write properties
    @property
    def params(self):
        return self._params
        
    @params.setter
    def params(self, obj):
        self._params = obj    
    
    @property
    def data(self):
        return self._data
        
    @data.setter
    def data(self, obj):
        self._data = obj

    # Methods
    def initialize(self):
        pass
    
    @abstractmethod
    def compute(self):
        """Algorithm perform the computation with the given data"""
    # end of def compute
        
# end of class Algorithm        


class Data(ContainerItem):
    def __init__(self):
        super().__init__()
        self._A = None
        self._n2i = None
        self._dg = None
        self._inputs= None
        self._df_ba = None
        self._df_exp = None


    # Read-only members
    @property
    def A(self): # Adjacency matrix
        return self._A

    @property
    def n2i(self): # Name to index mapping (hashable)
        return self._n2i

    @property
    def dg(self): # Directed graph object of NetworkX
        return self._dg

    @property
    def inputs(self): # Input conditions
        return self._inputs

    @property # DataFrame of basal activity
    def df_ba(self):
        return self._df_ba

    @property # DataFrame of experimental result
    def df_exp(self):
        return self._df_exp

# end of class Data