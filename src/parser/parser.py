
import ast
import astor
import sys, os
from typing import List

from src.ast import *

class Parser(ast.NodeVisitor):
    
    program: List[Statement] = []

    def __init__(self):
        pass
    
    
    def _extract_gaussian_from_call(self, node):
        """ Takes a call node as input and returns the mean and variance of a gaussian dist
        """

        #print(node.func.id)
        
        #function_ident = node.func.value.id
        #dist = node.func.attr
        dist = node.func.id
        if(dist != "Normal"):
            raise AssertionError("only allow gaussian distributions")

        
        if(isinstance(node.keywords[0].value, ast.BinOp)):
            #If we are here then this will be a CPD
            

            mean = self._create_bop(node.keywords[0].value)

            #No special care for the variance as this is fixed
            variance= node.keywords[1].value.value

        else:
            #If we are here then this will be a marginal distribution
            mean     = node.keywords[0].value.value
            variance = node.keywords[1].value.value
        
        return mean, variance


    def _construct_expr_for_bop(self, node):
        """ Constructs the left and right hand side for binary ops
        :returns: ast
        """

        if(isinstance(node, ast.Constant)):
            val = node.value
            if(isinstance(val, int)):
                return Integer(val) 
            if(isinstance(val, float)):
                return Real(val)
            raise TypeError("only support floats and integers")

        if(isinstance(node, ast.Name)):
            name = node.id
            return Ident(name)
        
        if(isinstance(node, ast.BinOp)):
            return self._create_bop(node)
        
        raise TypeError("unsupported binary operation")

    def _create_bop(self, node):
        """ constructs a binary operation
        :returns: ast
        """

        if(isinstance(node.op, ast.Add)):
            op = "+"
        elif(isinstance(node.op, ast.Mult)):
            op = "*"

        elif(isinstance(node.op, ast.Sub)):
            op = "-"

        elif(isinstance(node.op, ast.Div)):
            op = "/"

        else:
            raise TypeError("unsupported operation for binary operation")

        right = self._construct_expr_for_bop(node.right)
        left  = self._construct_expr_for_bop(node.left)
        return Bop(left, op, right)
    
    def _get_assign_from_loop(self, node):
        if(isinstance(node.targets[0], ast.Tuple)):
            raise AssertionError("Only assigning to a single value is allowed")
        
        name = node.targets[0].id
        rhs = node.value
        if(isinstance(rhs, ast.Call)):
            mean, variance = self._extract_gaussian_from_call(rhs)
            return Assign(Ident(name), Dist(mean, variance))
        
        elif(isinstance(rhs, ast.BinOp)):
            bop = self._create_bop(rhs)
            return Assign(Ident(name), bop)

        else:
            raise TypeError("Unsopported assignment")


    def visit_For(self, node):
        """ Visits every for loop node, and parses it into prob. ast
        :returns: Assign ast
        """

        num_iterations  = node.iter.args[0].value
        body = []
        for stmt in node.body:
            assign_node = self._get_assign_from_loop(stmt)
            body.append(assign_node)
        
        self.program.append(For(Integer(num_iterations), body))

    def visit_Assign(self, node):
        """ Visits every assign node, and parses it into prob. ast
        :returns: Assign ast
        """
        
        #The targets is a list. It will contain a Tuple in the case of assigning to multiple
        # variables (i.e. a,b = 5,4) and for simplicity we do not allow that for now
        if(isinstance(node.targets[0], ast.Tuple)):
            raise AssertionError("Only assigning to a single value is allowed")
        
        name = node.targets[0].id
        rhs = node.value
        if(isinstance(rhs, ast.Call)):
            mean, variance = self._extract_gaussian_from_call(rhs)
            self.program.append(Assign(Ident(name), Dist(mean, variance)))
        
        elif(isinstance(rhs, ast.BinOp)):
            bop = self._create_bop(rhs)
            self.program.append(Assign(Ident(name), bop))

        elif(isinstance(rhs, ast.Constant)):
            if(isinstance(rhs.value, int)):
                self.program.append(Assign(Ident(name), Integer(rhs.value)))
            else:
                self.program.append(Assign(Ident(name), Real(rhs.value)))
        else:
            raise TypeError("Unsopported assignment")

    
    def visit_Return(self, node):
        """ Visits every return node, and parses it into prob. ast
        :returns: Return ast
        """
        
        #We first only consider the case where we return a var as this i likely most interesting
        name = node.value.id
        self.program.append(Return(Ident(name)))
    
    def visit_Expr(self, node):
        """ Visits every expr node looking for calls that adds observations
        :returns Observe ast
        """


        if(isinstance(node.value, ast.Call)):
            list_of_arguments = node.value.args
            if(len(list_of_arguments) == 2):
                ident, expr = list_of_arguments 
                if(isinstance(expr, ast.UnaryOp)):
                    self.program.append(Condition(Ident(ident.value), Real(-expr.operand.value)))
                else:    
                    self.program.append(Condition(Ident(ident.value), Real(expr.value)))

            else:
                ident, expr, prec = list_of_arguments
                if(isinstance(expr, ast.UnaryOp)):
                    #We just assume that this means minus as it is not common to write ex- "+1"
                    if(isinstance(expr.operand.value, int)):
                        self.program.append(Observe(Ident(ident.value), Integer(-expr.operand.value), Real(prec.value)))
                    elif(isinstance(expr.operand.value, float)):
                        self.program.append(Observe(Ident(ident.value), Real(-expr.operand.value),Real(prec.value) ))
                    else:
                        raise AssertionError("unknown expresion in observation")

                elif(isinstance(expr.value, int)):
                    self.program.append(Observe(Ident(ident.value), Integer(expr.value),Real(prec.value) ))
                elif(isinstance(expr.value, float)):
                    self.program.append(Observe(Ident(ident.value), Real(expr.value),Real(prec.value) ))
                else:
                    raise AssertionError("unknown expresion in observation")
        else:
            raise AssertionError("Non-valid expression parsing error") 

def parse(filepath):
    """ The interface for parsing programs. Takes the filepath (str) as input
    :returns: ast

    """
    ast_tree   = ast.parse(open(filepath).read())
    parser     = Parser()

    # print(ast.dump(ast_tree))
    result_ast = parser.visit(ast_tree)
    # print(parser.program)
    
    return parser.program




