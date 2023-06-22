
""" This file contains the abstract syntax of the expressions in the ppl """

class Expr():
    
    def __init__(self):
        pass

    def to_string(self):
        pass

class Bop(Expr):
    
    """ The binary expression. Contains a left and right expression, and the operator as a string """

    left: Expr
    right: Expr
    op: str

    def __init__(self, left, op, right):
        self.left  = left
        self.right = right
        self.op    = op 
    
    def to_string(self):
        return self.op +  " lhs: " + self.left.to_string() + " rhs: " + self.right.to_string()

class Integer(Expr):
    
    """ Integer. Contains the value """

    val: int 

    def __init__(self, val):
        self.val = val
    
    def to_string(self):
        return str(self.val)

class Real(Expr):
    
    """ Float. Contains the value """
    
    val: float

    def __init__(self, val):
        self.val = val
    
    def to_string(self):
        return str(self.val)

class Ident(Expr):

    """ Identifier. A name for a variable """

    name: str

    def __init__(self, name):
        self.name = name
    
    def to_string(self):
        return self.name

class Dist(Expr):
    
    """ Gaussian distribution. Has mean and variance of distribution """

    mean: float
    variance: float

    def __init__(self, mean, variance):
        self.mean     = mean
        self.variance = variance
    
    def to_string(self):
        return "Gauss("+str(self.mean)+ " " + str(self.variance)+")"
