
"""
This file contains the abstract syntax of the statements in ppl

"""


from src.ast.expr import Expr, Ident
from typing import List

class Statement():
    

    def __init__(self):
        pass

    def print(self):
        pass

class For(Statement):
    
    """ For loops. They contain the body of the loop and number of iterations  """
    
    num: Expr
    body: List[Statement]
    
    def __init__(self, num, body):
        self.num = num
        self.body = body
    
class Assign(Statement):
    
    """ Assignments. Contains an identifier and an expression """

    lhs: Ident 
    rhs: Expr
    
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def print(self):
        print("assignment with lhs: " + self.lhs.to_string() + "and rhs: " + self.rhs.to_string())


class Return(Statement):
    
    """Return. Contains the expression (a variable/value) to return """

    expr: Expr

    def __init__(self, expr):
        self.expr = expr

    def print(self):
        print("return " + self.expr.to_string())


class Observe(Statement):

    """ Observation. Contains the identifier of the observed variable. Also containrs the mean and presision of the observation """

    ident: Ident
    expr:  Expr
    precision: Expr
    def __init__(self, ident, expr, precision):
        """TODO: to be defined. """

        self.ident = ident
        self.expr  = expr
        self.precision = precision

    def print(self):
        print("")


class Condition(Statement):
    
    """ Condition. An exact conditioning of a random variable """

    ident: Ident
    expr: Expr 

    def __init__(self, ident, expr):

        self.ident = ident 
        self.expr = expr 
    
    def print(self):
        print("")
