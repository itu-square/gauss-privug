
from typing import Dict, List, NewType, Tuple
from src.ast import *
from src.dist import *
from tqdm import tqdm

env: Dict[str, Expr] = {}
distribution = NewType("dist", Tuple[float, float])

multivariant_joint_distribution = MultivariateDist({}, {}) 

observations: Dict[str, float] = {}

name_to_index: Dict[str, int] = {}
index_to_name: Dict[int, str] = {}

#global primitive values
global index
index: int
index = 0

global current_name_left
current_name_left: str 
current_name_left = ""

global current_name_right
current_name_right: str
current_name_right = ""

global num_iterations_loop
num_iterations_loop: int
num_iterations_loop = 0

def _bop_val_dist(op, val, distribution):
    """ A helper function for evaluating distributions and values
    :returns: tuple of updated mean and variance
    """
    mean, variance = distribution

    #print("in here")
    #print(multivariant_joint_distribution.covariance_matrix)
    #print(multivariant_joint_distribution.mean_vector)
    if(op == "+"):
        mean1 = mean + val
        return (mean1, variance)
    
    elif(op == "*"):
     
        mean1     = mean * val
        variance1 = variance * (val**2)
        return (mean1, variance1)

    
    elif(op == "/"):
        #print(distribution)
        mean1     = mean / val
        variance1 = variance * ((1/val)**2)
        return (mean1, variance1)

    
    else:
        mean1 = mean - val
        return (mean1, variance)
    

def _bop_val_val(op, val1, val2):    
    if(op == "+"):
        res = val1 + val2
        return res
    
    elif(op == "-"):
        res = val1 - val2
        return res

    elif(op == "/"):
        res     = val1 / val2
        return res

    
    elif(op == "*"):
        res     = val1 * val2
        return res
    
    else:
        res = val1 - val2
        return res
    

def _bop_dist_dist(op, distribution1, distribution2):
    #print("op here")
    mu1, std1 = distribution1
    mu2, std2 = distribution2
    if(op == "+"):
        mu3  = mu1 + mu2
        std3 = std1 + std2
        return (mu3, std3)

    elif(op == "*"):
        mu3 = mu1 * mu2
        std3 = std1 * std2
        return (mu3, std3)
    
    elif(op == "/"):
        mu3 = mu1 / mu2
        std3 = std1 / std2
        return (mu3, std3)

    elif(op == "-"):
        mu3  = mu1 - mu2  
        std3 = std1 + std2
        return (mu3, std3)
    else:
        raise TypeError("Error in bop dist dist")
        #return -1


### HELPER FUNCTIONS #########
def _find_strength_relation(bop):
    
    if(bop.op == "*"):
        if(isinstance(bop.left, Integer) or isinstance(bop.left, Real) ):
            return bop.left.val

        if(isinstance(bop.right, Integer) or isinstance(bop.right, Real)):
            return bop.right.val
    if(isinstance(bop.left, Bop)):
        return _find_strength_relation(bop.left)

    if(isinstance(bop.right, Bop)):
        return _find_strength_relation(bop.right)


def _find_dependent_name(bop):
    if(isinstance(bop.left, Ident)):
        return bop.left.name
    if(isinstance(bop.right, Ident)):
        return bop.right.name
    else:
        if(isinstance(bop.left, Bop)):
            return _find_dependent_name(bop.left)
        return _find_dependent_name(bop.right)



def _update_multivariant_dist(res, new_name, old_name):
   


    mean = res[0]
    multivariant_joint_distribution.mean_vector[new_name] = mean
    
    set_variables = []
    variance = multivariant_joint_distribution.covariance_matrix[old_name+"-"+old_name]
    cov_matrix_keys = list(multivariant_joint_distribution.covariance_matrix.keys()).copy()
    for cov in cov_matrix_keys:
        if old_name in cov:
            values   = cov.split("-")
            var1      = values[0]
            var2      = values[1]
            if(old_name == var1):
                variable = var2
            else:
                variable = var1

            if(variable in set_variables or variable == ""):
                continue

            cov_val = multivariant_joint_distribution.covariance_matrix[old_name+"-"+variable]
            multivariant_joint_distribution.covariance_matrix[new_name+"-"+variable] = cov_val
            multivariant_joint_distribution.covariance_matrix[variable+"-"+new_name] = cov_val
            set_variables.append(variable)
    
    #set variance and covariance between the two nodes 
    multivariant_joint_distribution.covariance_matrix[new_name+"-"+new_name] = variance + 1 
    multivariant_joint_distribution.covariance_matrix[old_name+"-"+new_name] = variance
    multivariant_joint_distribution.covariance_matrix[new_name+"-"+old_name] = variance
    

def _update_multivariant_dist_indep_dist(name, left_name, right_name, res):

   
    mean    = res[0]
    variance = res[1]

    #print("inside the update cov for independent dists..")
    #print(left_name)
    #print(right_name)
    
    left_variance = multivariant_joint_distribution.get_variance(left_name)
    right_variance = multivariant_joint_distribution.get_variance(right_name)
    multivariant_joint_distribution.mean_vector[name] = mean

    #We need to conside that the left hand side already exists and then do an update instead
    if(name+"-"+name in multivariant_joint_distribution.covariance_matrix):
        #print("here....")
        #print(name)
        #print(left_name)
        if(name==left_name):
            new_variance = right_variance
        
        elif(name==right_name):
            new_variance = left_variance
        else:
            new_variance = left_variance + right_variance
        old_variance = multivariant_joint_distribution.covariance_matrix[name+"-"+name]
        multivariant_joint_distribution.covariance_matrix.update({name+"-"+name: new_variance + old_variance})

    else:
        multivariant_joint_distribution.covariance_matrix[name+"-"+name] = variance + left_variance + right_variance
    
    if(left_name == name):

        multivariant_joint_distribution.covariance_matrix[right_name+"-"+name] = right_variance
        multivariant_joint_distribution.covariance_matrix[name+"-"+right_name] = right_variance
    
    elif(right_name == name):
        multivariant_joint_distribution.covariance_matrix[left_name+"-"+name] = left_variance
        multivariant_joint_distribution.covariance_matrix[name+"-"+left_name] = left_variance
    else:
        multivariant_joint_distribution.covariance_matrix[right_name+"-"+name] = right_variance
        multivariant_joint_distribution.covariance_matrix[name+"-"+right_name] = right_variance

        multivariant_joint_distribution.covariance_matrix[left_name+"-"+name] = left_variance
        multivariant_joint_distribution.covariance_matrix[name+"-"+left_name] = left_variance

    set_variables_left  = []
    set_variables_right = []
    


    
    
##############################

def evaluate_expr(name:str, expr:Expr, from_dist_eval:bool):
    """ A helper function for evaluating expressions
    :returns: TODO
    """
    global index 
    global current_name_left
    global current_name_right

    #print("evaluating expression")
    #print(expr)
    #print(name)
    
    if(isinstance(expr, Integer)):
        return expr.val
    
    if(isinstance(expr,Real)):
        return expr.val
    
    if(isinstance(expr,Ident)):

        if(expr.name in name_to_index.keys()):

            idx  = name_to_index[expr.name]
            var  = multivariant_joint_distribution.covariance_matrix[expr.name+"-"+expr.name]
            mean = multivariant_joint_distribution.mean_vector[expr.name]
            return(mean, var)
        else:
            val = env[expr.name]
            return val

    if(isinstance(expr,Dist)):
        mean     = expr.mean
        variance = expr.variance
        name_to_index[name] = index
        index_to_name[index] = name
        index += 1
        if(isinstance(mean, Bop)):

            strength  = _find_strength_relation(mean)
            dependent = _find_dependent_name(mean)
            dependent_variance = multivariant_joint_distribution.covariance_matrix[dependent+"-"+dependent]

            mean         = evaluate_expr(name, mean, True)[0]
            multivariant_joint_distribution.mean_vector[name] = mean

            variance = variance + (strength**2) * dependent_variance
            multivariant_joint_distribution.covariance_matrix[name+"-"+name] = variance
            
            multivariant_joint_distribution.covariance_matrix[dependent+"-"+name] = strength*dependent_variance
            multivariant_joint_distribution.covariance_matrix[name+"-"+dependent] = strength*dependent_variance
            
            cov_matrix_keys = list(multivariant_joint_distribution.covariance_matrix.keys()).copy()
            for cov in cov_matrix_keys:
                if dependent in cov:
                    variance = multivariant_joint_distribution.covariance_matrix[cov]
                    #var      = cov.replace(dependent, "")
                    values   = cov.split("-")
                    var1      = values[0]
                    var2      = values[1]
                    if(dependent == var1):
                        var = var2
                    else:
                        var = var1
                    if(var == ""):
                        continue
                    if(name == var):
                        continue

                    cov_val = multivariant_joint_distribution.covariance_matrix[dependent+"-"+var]
                    multivariant_joint_distribution.covariance_matrix[name+"-"+var] = strength * cov_val
                    multivariant_joint_distribution.covariance_matrix[var+"-"+name] = strength * cov_val

        else:
            multivariant_joint_distribution.mean_vector[name] = mean
            multivariant_joint_distribution.covariance_matrix[name+"-"+name] = variance

        return (mean, variance)

    if(isinstance(expr, Bop)):
        left  = expr.left
        right = expr.right
        #print("expression is a bop")
        #print(left)
        #print(right)
        if(isinstance(right, Ident)):
            current_name_right = right.name
        
        if(isinstance(left, Ident)):
            current_name_left =  left.name
        
        op    = expr.op
        left1  = evaluate_expr(name, left, True)


        right1 = evaluate_expr(name, right, True)
        
        if(isinstance(left1, Dist)):
            mean, variance = evaluate_expr(name, left1, True)
            if(isinstance(right1, Dist)):
                
                mean1, variance1 = evaluate_expr(name, right1, True)
                res = _bop_dist_dist(op, (mean, variance), (mean1, variance1))
                return res
            else:
                print("here...")
                res = _bop_val_dist(op, right1, (mean, variance))
                return res
        
        elif(isinstance(right1, Dist)):
            mean, variance = evaluate_expr(name, right1, True)
            if(isinstance(left1, Dist)):
                mean1, variance1 = evaluate_expr(name, left1, True)
                res = _bop_dist_dist(op, (mean, variance), (mean1, variance1))
                return res
            else:
                val = evaluate_expr(name, left1, False)
                res = _bop_val_dist(op, val, (mean, variance))
                return res
               
        else:
            if(isinstance(left1, tuple)):
                if(isinstance(right1, tuple)):
                    #print("both left and right are tuples")
                    #print(current_name_left)
                    #print(current_name_right)
                    res = _bop_dist_dist(op, left1, right1)
                    _update_multivariant_dist_indep_dist(name, current_name_left, current_name_right, res)
                    if(not (name == current_name_left or name == current_name_right)):
                        
                        name_to_index[name] = index
                        index_to_name[index] = name
                        index+=1
                        
                    return res
                else:
                     #print("asdhjashd")
                     res  = _bop_val_dist(op, right1, left1)
                     #print(right1)
                     #print(left1)
                     mean = res[0]
                     var  = res[1]
                     multivariant_joint_distribution.mean_vector[name] = mean
                     multivariant_joint_distribution.covariance_matrix[name+"-"+name] = var

                     #update all the covariances as well:

                     for key in multivariant_joint_distribution.covariance_matrix:
                         if(name in key and not (name+"-"+name in key)):
                             multivariant_joint_distribution.covariance_matrix[key] =  multivariant_joint_distribution.covariance_matrix[key] * ((1/right1)**2)
                     
                     if(not (name == current_name_left or name == current_name_right) and not from_dist_eval):
                        name_to_index[name] = index
                        index_to_name[index] = name
                        index+=1
                     return res
            if(isinstance(right1, tuple)):
                if(isinstance(left1, tuple)):
                    res = _bop_dist_dist(op, left1, right1)
                    _update_multivariant_dist_indep_dist(name, current_name_left, current_name_right, res)
                    if(not (name == current_name_left or name == current_name_right)):
                        name_to_index[name] = index
                        index_to_name[index] = name
                        index+=1
                    return res
                else:
                    res = _bop_val_dist(op, left1, right1)
                    _update_multivariant_dist(res, name, current_name_right)

                    if(not (name == current_name_left or name == current_name_right) and not from_dist_eval ):
                        name_to_index[name] = index
                        index_to_name[index] = name
                        index+=1
                    return res
            else:
                res = _bop_val_val(op, left1, right1)
                return res

def evaluate_loop(stmt: Statement, num_iterations:int):
    global index
    global name_to_index
    global index_to_name
    
    if(print_state):
        print("inside loop evaluation !!!!!")

    if(len(stmt)> 1):
        raise TypeError("only single statment in loop")
    statement = stmt[0]
    variable_to_unroll = ""
    if(not isinstance(statement, Assign)):
        raise TypeError("only assignments in loop")
    variable = statement.lhs.name
    
    variable_mean = multivariant_joint_distribution.mean_vector[variable]
    variable_var  = multivariant_joint_distribution.covariance_matrix[variable+"-"+variable]
    updated_variable_var = variable_var
    
    bop      = statement.rhs
    left_variable = bop.left.name
    right_variable = bop.right.name
    if(variable == left_variable):
        variable_to_unroll = right_variable
    elif(variable == right_variable):
        variable_to_unroll = left_variable
    else:
        raise TypeError("unknown variable")

    
    variable_to_unroll_mean = multivariant_joint_distribution.mean_vector[variable_to_unroll]
    variable_to_unroll_var  = multivariant_joint_distribution.covariance_matrix[variable_to_unroll+"-"+variable_to_unroll]
    
    for i in range(num_iterations):
        new_name = str(index)
        updated_variable_var += variable_to_unroll_var
        #print(updated_variable_var)
        variable_mean += variable_to_unroll_mean
        multivariant_joint_distribution.mean_vector[new_name] = variable_to_unroll_mean
        multivariant_joint_distribution.covariance_matrix[new_name+"-"+new_name] = variable_to_unroll_var
        multivariant_joint_distribution.covariance_matrix[new_name+"-"+variable] = variable_to_unroll_var + variable_var
        multivariant_joint_distribution.covariance_matrix[variable+"-"+new_name] = variable_to_unroll_var + variable_var
        name_to_index[new_name] = index
        index_to_name[index] = new_name
        index+=1
    
    print(index)
    
    #print(name_to_index)
    multivariant_joint_distribution.mean_vector[variable] = variable_mean
    multivariant_joint_distribution.covariance_matrix[variable+"-"+variable] = updated_variable_var
    multivariant_joint_distribution.covariance_matrix[variable+"-"+variable_to_unroll] = variable_to_unroll_var + variable_var
    multivariant_joint_distribution.covariance_matrix[variable_to_unroll+"-"+variable] = variable_to_unroll_var + variable_var
    
    #print(multivariant_joint_distribution.covariance_matrix)

    variable_index = name_to_index[variable]

    name_to_index.update({variable: index-1})
    name_to_index.update({str(index-1): variable_index})
    
    index_to_name.update({index-1: variable})
    index_to_name.update({variable_index: str(index-1)})
    index+=1
    #print(name_to_index)
    if(print_state):
        print("finsished loop evaluation !!!!!")
def remove_val_from_dist(val):

    global index

    #print(name_to_index)
    #print(index)
    
    name_to_index.pop(val, None)
    index = index - 1
    
    #print(name_to_index)
    #print(index)
    keys_to_pop = [] 
    for cov in multivariant_joint_distribution.covariance_matrix.keys():
        if(val in cov):
            keys_to_pop.append(cov)
            
    for key in keys_to_pop:
        multivariant_joint_distribution.covariance_matrix.pop(key, None)

    multivariant_joint_distribution.mean_vector.pop(val, None)

def condition_distribution(ident, expr):
    
    #print("inside condition function from the eval") 
    #print(multivariant_joint_distribution.mean_vector)
    #print(multivariant_joint_distribution.covariance_matrix)


    #TODO Implement this function
    multivariant_joint_distribution.condition(ident, expr, name_to_index, index_to_name, index)
    
    remove_val_from_dist(ident)
    
    env[ident] = expr
    
    #print(multivariant_joint_distribution.mean_vector)
    #print(multivariant_joint_distribution.covariance_matrix)
    

    #print("finished with condition function from the eval") 

def evaluate(program: List[Statement]) -> distribution: 
    """ The eval main evaluation loop. Runs through each statement in the and updates the state
    :returns: Gaussian distribution
    """     
    global index
    
    for stmt in program:
        if(isinstance(stmt, For)):
            evaluate_loop(stmt.body, stmt.num.val)
        elif(isinstance(stmt, Assign)):
            lhs  = stmt.lhs.name
            rhs  = stmt.rhs
            if(isinstance(rhs, Dist)):
                rhs1 = evaluate_expr(lhs, rhs, True)
            else:
                rhs1 = evaluate_expr(lhs, rhs, False)
            env[lhs] = rhs1
        elif(isinstance(stmt, Observe)):
            observations[stmt.ident.name] = (stmt.expr.val, stmt.precision.val)
        elif(isinstance(stmt, Condition)):
            #print(stmt.ident.name)
            #print(stmt.expr.val)
            condition_distribution(stmt.ident.name, stmt.expr.val)
        elif(isinstance(stmt, Return)):
            expr = stmt.expr
            #assume identifier
            name = expr.name
            val  = env[name]
            #print(multivariant_joint_distribution.covariance_matrix)
            
            #index+=1
            multivariant_joint_distribution.to_np(name_to_index, index)
            
            #multivariant_joint_distribution.construct_information_form()
            #multivariant_joint_distribution.add_observations(observations, name_to_index)
            
            #print('3')
            #print(multivariant_joint_distribution.potential_vector)
            #print(multivariant_joint_distribution.precision_matrix)
            
            mean, variance = multivariant_joint_distribution.marginalize(name, name_to_index, index)            
            return distribution((mean, variance))
        else:
            raise TypeError("unknown statement")
    #Missing return statement
    return distribution((-1,-1))



