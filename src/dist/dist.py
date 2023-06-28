
from typing import List, Dict
import numpy as np
import math
from tqdm import tqdm
from numba import jit


#@jit(nopython=True)
#def update_cov_matrix_map(matrix_dim, index_1, index_to_name, covariance_matrix_np, covariance_keys):
 #   result = np.array([])
  #  for j in range(matrix_dim):
   #     name_1 = index_to_name[index_1]
    #    name_2 = index_to_name[j]
      #  val = covariance_matrix_np[index_1][j]
       # key = str(name_1) + "-" + str(name_2)
        #if(key in covariance_keys):
         #   result.append((key, val))
            #self.covariance_matrix.update({key:val})
    #return result 


 # name_1 = index_to_name[index_1]
  #      name_2 = index_to_name[index_2]
   #     key = str(name_1) + "-" + str(name_2)
    #    val = covariance_matrix_np[index_1][index_2]
     #   if(key in covariance_keys):
      #      covariance_matrix.update({key:val})            

print_state = False


class MultivariateDist():
   
    """
    This class is a representation of the entire multivariate Gaussian distribution.
    It has methods for converting from covariance form to information form.
    The Gaussian belief propagation algorithm is defined in this file as part of the marginalization.
    """
    #Covariance form for parsing
    mean_vector: Dict[str,float]
    covariance_matrix: Dict[str,float]
    
    #Covariance form for propagation
    mean_vector_np: List[float]
    covariance_matrix_np: List[List[float]]
    
    #Information form 
    potential_vector: List[float]
    precision_matrix: List[List[float]]
    
    messages_received_mean: Dict[int, List[int]]
    messages_received_variance: Dict[int, List[int]]

    observed_indices: List[int]

    def __init__(self, vec, cov):
        self.mean_vector       = vec
        self.covariance_matrix = cov
        self.messages_received_mean = {}
        self.messages_received_variance = {}
        self.observed_indices = []

    def construct_information_form(self):
        """
        Converts from covaraince form to information form.
        """
        #print(self.mean_vector)
        #print(self.covariance_matrix)
        print(self.covariance_matrix_np)
        self.precision_matrix = np.linalg.inv(self.covariance_matrix_np)
        self.potential_vector = np.matmul(self.precision_matrix, self.mean_vector_np)
   
    def get_variance(self, name):
        return self.covariance_matrix[name+"-"+name]


    def add_observations(self, observations, name_to_index):
        """
        Add observations to the distribution.
        """

        #print(observations)
        #print(self.potential_vector)
        observed_indices = []
        for obs_variable in observations.keys():
            obs = observations[obs_variable]
            mean = obs[0]
            var  = obs[1]
            obs_idx = name_to_index[obs_variable]
            observed_indices.append(obs_idx)
            self.potential_vector[obs_idx] = self.potential_vector[obs_idx] + mean
            self.precision_matrix[obs_idx][obs_idx] = var + self.precision_matrix[obs_idx][obs_idx]

            #print(self.potential_vector)
        
        self.observed_indices = observed_indices
    
    def _find_neighbors(self, node, max_index):
        neighbors = []
        for i in range(max_index):
            cov = self.precision_matrix[node][i]
            if(cov == 0 or i == node):
                continue
            neighbors.append(i)
        
        return neighbors
    
    def condition(self, name, val, name_to_index, index_to_name, max_index):
        """
        Conditions a distribution on an exact observation
        """
        #print(name_to_index)
        #print("inside the condition function")
        #print(max_index)
        #print(name_to_index)
        if(print_state):
            print("inside the conditioning function")
        #print(self.covariance_matrix)
        mean_vector, covariance_matrix = self.to_temp_np(name_to_index, max_index)
 
        #print(name_to_index)
        #print(max_index-1)
        
        #print(name)
        #print("inside condition function")
        #print(mean_vector)
        #print(covariance_matrix)
        
        if(print_state):
            print(mean_vector)
            print(covariance_matrix)

        #print(mean_vector)
        #print(covariance_matrix)

        
        var_of_obs = covariance_matrix[max_index-1][max_index-1]
        #print(var_of_obs)
        #print(var_of_obs)
        covariance_vector = covariance_matrix[max_index-1, 0:max_index-1]
        #print(covariance_vector)
        covariance_vector = covariance_vector.reshape(max_index-1,1) 
        old_covariance_matrix = covariance_matrix[0:max_index-1, 0:max_index-1]
        #print(old_covariance_matrix)
        #print( (1/var_of_obs) * np.dot(covariance_vector, covariance_vector.T))
        updated_covariance_matrix = old_covariance_matrix - (1/var_of_obs) * np.dot(covariance_vector, covariance_vector.T)
        #print(updated_covariance_matrix)
        #print(mean_vector[0:max_index-1])
        #print(covariance_vector.T)
        updated_mean_vector = mean_vector[0:max_index-1] + (((val-mean_vector[max_index-1]) / var_of_obs) * covariance_vector.T)
        #print(updated_mean_vector)
        #print("done with conditioning function")

        self.update_state_from_np(updated_mean_vector, updated_covariance_matrix, name_to_index,index_to_name, max_index)

        

        #return (updated_mean_vector, updated_covariance_matrix)
    

    def index_to_name(self, name_to_index, index):
        name =list(name_to_index.keys())[list(name_to_index.values()).index(index)]
        return name
        



    def update_state_from_np(self, mean_vector_np, covariance_matrix_np, name_to_index,index_to_name, max_index):
        #print("inside update state")
        #Update mean vector
        mean_vector_np = mean_vector_np[0]
        covariance_keys = np.array(list(self.covariance_matrix.keys()))
        for i in range(len(mean_vector_np)):
            val = mean_vector_np[i]
            name = self.index_to_name(name_to_index, i)
            self.mean_vector.update({name:val})
        
        #Update covariance_matrix
        
        matrix_dim = len(covariance_matrix_np[0])
        #TODO THIS IS SLOW. Updating a dictionary in a nested loop like this is not good!
        for i in range(matrix_dim):
            #update_cov_matrix_map(matrix_dim, i, index_to_name, covariance_matrix_np, covariance_keys)
            for j in range(matrix_dim):

                #update_cov_matrix_map(self.covariance_matrix, i, j, index_to_name, covariance_keys) 
                name_1 = index_to_name[i]
                name_2 = index_to_name[j]
                val = covariance_matrix_np[i][j]
                key = str(name_1) + "-" + str(name_2)
                #update_cov_matrix_map(self.covariance_matrix, i, j, index_to_name,covariance_matrix_np, covariance_keys)
                #if(res is not None):
                 #   self.covariance_matrix.update({res:val})
                #else:
                 #   continue
                #key = str(name_1) + "-" + str(name_2)
                if(key in covariance_keys):
                    #self.covariance_matrix.update({key:val})
                    self.covariance_matrix[key] = val

        #print("done with update state")

    def marginalize(self, name, name_to_index, max_index):
        """
        Runs the BP algorithm by solving a set of linear equations.
        Returns the marginal posterior distrbution
        """
        marginal_index = name_to_index[name]
        #print(self.potential_vector)
        #print(self.precision_matrix)
        #posterior_covariance  = np.linalg.inv(self.precision_matrix)
        #posterior_mean_vector = np.matmul(posterior_covariance, np.array(self.potential_vector))
        #if(print_state):
        #print(self.covariance_matrix_np)
        #printp(self.mean_vector_np)


        #This returns the marginal without BP
        #mean                  = self.mean_vector_np[marginal_index]
        #variance              = self.covariance_matrix_np[marginal_index][marginal_index]

        #This returns the marginal with BP
        #mean                  = posterior_mean_vector[marginal_index]
        #variance              = posterior_covariance[marginal_index][marginal_index]

        #return mean, variance

        #Change to return entire multivariate dist
        #TODO in the future we should return the sub-vector specified in the return stmt.
        #print(self.mean_vector_np)
        #print(self.covariance_matrix_np)
        return (self.mean_vector_np, self.covariance_matrix_np)
    

    def to_temp_np(self, name_to_index, max_index):
        """
        Convenience function for turning into numpy array without settting the fields of the class
        """

        #print("inside the to temp np function")
        mean_vector_np = np.zeros(max_index) 
        covariance_matrix_np = np.zeros((max_index, max_index)) 
        for name in name_to_index.keys():
            idx = name_to_index[name]
            val = self.mean_vector[name]
            mean_vector_np[idx] = val
            for cov in self.covariance_matrix.keys():
                if(name in cov):
                    val = self.covariance_matrix[cov]
                    if(name+"-"+name in cov):
                        covariance_matrix_np[idx][idx] = val
                    else:
                        names = cov.split("-")
                        first  = names[0]
                        second = names[1]
                        idx_first  = name_to_index[first]
                        idx_second = name_to_index[second]
                        covariance_matrix_np[idx_first][idx_second] = val
        
        #print("done with the to temp np function")
        
        return (mean_vector_np, covariance_matrix_np)

    def to_np(self, name_to_index, max_index):
        """
        Convenience funtion for turning into numpy array
        """
        #print("inside the to np function") 
        #print(self.covariance_matrix)
        #print(max_index)
        #print(name_to_index)
        self.mean_vector_np = np.zeros(max_index) 
        self.covariance_matrix_np = np.zeros((max_index, max_index)) 
        for name in name_to_index.keys():
            #print(name)
            idx = name_to_index[name]
            val = self.mean_vector[name]
            self.mean_vector_np[idx] = val
            #print(self.covariance_matrix.keys())
            for cov in self.covariance_matrix.keys():
                if(name in cov):
                    val = self.covariance_matrix[cov]
                    if(name+"-"+name in cov):
                        self.covariance_matrix_np[idx][idx] = val
                    else:
                        names = cov.split("-")
                        first  = names[0]
                        second = names[1]
                        idx_first  = name_to_index[first]
                        idx_second = name_to_index[second]
                        self.covariance_matrix_np[idx_first][idx_second] = val
