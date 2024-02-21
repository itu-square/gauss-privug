
from typing import Dict, List, NewType, Tuple
from src.ast import *
from src.dist import *

distribution = NewType("dist", Tuple[float, float])

env: Dict[str, Expr] = {}

#Init the multivariate Gaussian distribution with a zero mean vector and zero covariance
mg_dist = MultivariateDist(np.array([]), np.array([]).reshape(0,0)) 

#Keep track of the names and indices for distributions
name_to_index: Dict[str, int] = {}
index_to_name: Dict[int, str] = {}

#global index
global index
index = 0

def evaluate_condition(name:str, val:Expr):
    global index
    rv_obs_index = name_to_index[name]
    mg_dist.condition(val, rv_obs_index, index)
    
    #We remove the observed variable from the distribution
    del name_to_index[name]
    del index_to_name[rv_obs_index]
    index = index - 1
    
def evaluate_expression(name:str, expr:Expr):
    print("TODO")
    
def evaluate_expression_ind_dist(name:str, expr:Expr):
    global index
    mg_dist.update_mean_vector_ind_assignment(expr.mean)
    mg_dist.update_covariance_ind_assignment(expr.variance, index)
    name_to_index[name] = index
    index_to_name[index] = name
    index = index + 1
  
def evaluate_expression_bop_assignment(name:str, bop:Expr):
    global index
    if((not isinstance(bop.left, Bop)) and not (isinstance(bop.left, Bop))):
        #Not a nested binary expression.
        #We support 2 types of bop assigments for now. Namely Y = 0.1 * X wher X is and identifier that already exists or = Y = X + Z where X can be existing val
        if(isinstance(bop.left, Ident)):
            rv_name_left  = bop.left.name
            rv_name_right = bop.right.name
            left_index  = name_to_index[rv_name_left]
            right_index = name_to_index[rv_name_right]
            if(rv_name_left == name):
                # Y = Y op Z
                mg_dist.update_mean_vector_p_sum_exists(left_index, right_index)
                mg_dist.update_covariance_matrix_p_sum_exists(left_index, right_index, index)
                
            else:
                # Y = X op Z
                mg_dist.update_mean_vector_p_sum(left_index, right_index)
                mg_dist.update_covariance_matrix_p_sum(left_index, right_index, index)
                name_to_index[name] = index
                index_to_name[index] = name
                index = index + 1
        else:
            #Y = n op X
            value       = bop.left.val
            rv_name     = bop.right.name
            index_of_rv = name_to_index[rv_name]
            if(bop.op == "+"):
                mg_dist.update_mean_vector_p_op_pm(index_of_rv, value, True)
                mg_dist.update_covariance_matrix_p_op_pm(index_of_rv, index, value)
                name_to_index[name] = index
                index_to_name[index] = name
                index = index + 1
            elif(bop.op == "-"):
                mg_dist.update_mean_vector_p_op_pm(index_of_rv, value, False)
                mg_dist.update_covariance_matrix_p_op_pm(index_of_rv, index, value)
                name_to_index[name] = index
                index_to_name[index] = name
                index = index + 1
            elif(bop.op == "*"):
                mg_dist.update_mean_vector_p_op_md(index_of_rv, value)
                mg_dist.update_covariance_matrix_p_op_md(index_of_rv,index, value)
                name_to_index[name] = index
                index_to_name[index] = name
                index = index + 1
            else:
                raise TypeError("Unknown operator")
    else:
        #A nested binary expression
        print("a")


def evaluate(program: List[Statement]) -> distribution: 
    """ The eval main evaluation loop. Runs through each statement in the and updates the state
    :returns: Gaussian distribution
    """     
    global index

    for stmt in program:
        if(isinstance(stmt, For)):
            loop_count = stmt.num.val
            for i in range(loop_count):
                evaluate(stmt.body)
        elif(isinstance(stmt, Assign)):
            name  = stmt.lhs.name
            rhs  = stmt.rhs
            if(isinstance(rhs, Bop)):
                #The right hand side of assigment is a binary operator
                evaluate_expression_bop_assignment(name, rhs)
            elif(isinstance(rhs, Dist)):
                #The right hand side of assignment is a dist. For now this is always an inpendent dist
                rhs1 = evaluate_expression_ind_dist(name, rhs)
            else:
                rhs1 = evaluate_expr(name, rhs)
                env[lhs] = rhs1
        elif(isinstance(stmt, Condition)):
            #condition_distribution(stmt.ident.name, stmt.expr.val)
            evaluate_condition(stmt.ident.name, stmt.expr.val)
        elif(isinstance(stmt, Return)):
            return (mg_dist.mean_vector, mg_dist.covariance_matrix)
        else:
            raise TypeError("unknown statement")
    #Missing return statement
    return distribution((-1,-1))




