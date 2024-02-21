
from typing import List, Dict
import numpy as np
import math

class MultivariateDist():
 
    observed_indices: List[int]

    def __init__(self, vec, cov):
        self.mean_vector       = vec
        self.covariance_matrix = cov

    def get_variance(self, index):
        return self.covariance_matrix[index][index]
    
    def get_mean(self, index):
        return self.mean_vector[index]

    def update_mean_vector_ind_assignment(self, mean):
        self.mean_vector = np.append(self.mean_vector,mean)

    def update_covariance_ind_assignment(self, variance, index):
        #Pad with zero row and column vector
        self.covariance_matrix = np.pad(self.covariance_matrix, [(0, 1), (0, 1)], 'constant', constant_values=0)
        #Set the variance for the new entry
        self.covariance_matrix[index][index] = variance
        #Update the dimensions
        self.covariance_matrix = self.covariance_matrix.reshape(index+1, index+1)

    def update_mean_vector_p_op_pm(self, index, value, plus):
        if(plus):
            self.mean_vector = np.append(self.mean_vector, self.mean_vector[index] + value)
        else:
            self.mean_vector = np.append(self.mean_vector, self.mean_vector[index] - value)
            
    def update_covariance_matrix_p_op_pm(self, index_rv,index, value):
        #Comput new row and col vector
        covariance_vector = self.covariance_matrix[index_rv] 
        new_variance      = self.covariance_matrix[index_rv][index_rv] 
        new_row           = np.append(covariance_vector, new_variance)

        self.covariance_matrix = np.pad(self.covariance_matrix, [(0, 1), (0, 1)], 'constant', constant_values=0)
        self.covariance_matrix[index:] = new_row
        self.covariance_matrix[:,index] = new_row
        
        self.covariance_matrix = self.covariance_matrix.reshape(index+1, index+1)
    
    def update_mean_vector_p_op_md(self, index, value):
        self.mean_vector = np.append(self.mean_vector, self.mean_vector[index] * value)
        
    def update_covariance_matrix_p_op_md(self, index_rv, index, value):
        #Compute new row and col vector
        covariance_vector = self.covariance_matrix[index_rv] * value
        new_variance      = self.covariance_matrix[index_rv][index_rv] * value**2
        new_row           = np.append(covariance_vector, new_variance)

        #Pad with zeros and set them to new row and col vector
        self.covariance_matrix = np.pad(self.covariance_matrix, [(0, 1), (0, 1)], 'constant', constant_values=0)
        self.covariance_matrix[index:] = new_row
        self.covariance_matrix[:,index] = new_row
        
        self.covariance_matrix = self.covariance_matrix.reshape(index+1, index+1)
      
    def update_mean_vector_p_sum(self, left_index, right_index):
        new_mean = self.mean_vector[left_index] + self.mean_vector[right_index]
        self.mean_vector = np.append(self.mean_vector, new_mean)

    def update_covariance_matrix_p_sum(self, left_index, right_index, index):
        new_variance = self.covariance_matrix[left_index][left_index] +self.covariance_matrix[right_index][right_index] +self.covariance_matrix[right_index][left_index] +  self.covariance_matrix[left_index][right_index]

        new_row     = np.append(self.covariance_matrix[left_index] + self.covariance_matrix[right_index], new_variance)
        self.covariance_matrix = np.pad(self.covariance_matrix, [(0, 1), (0, 1)], 'constant', constant_values=0)
        self.covariance_matrix[index:] = new_row
        self.covariance_matrix[:,index] = new_row
        self.covariance_matrix = self.covariance_matrix.reshape(index+1, index+1)

    def update_mean_vector_p_sum_exists(self, left_index, right_index):
        # p sum rule for a RV that already exists
        self.mean_vector[left_index] =  self.mean_vector[left_index] + self.mean_vector[right_index]

    def update_covariance_matrix_p_sum_exists(self, left_index, right_index, index):
        #p sum rule for a RV that already exists
        new_covariance_vector = self.covariance_matrix[left_index] + self.covariance_matrix[right_index]        
        self.covariance_matrix[left_index:] = new_covariance_vector
        self.covariance_matrix[:,left_index] = new_covariance_vector
        
        self.covariance_matrix[left_index][left_index] =  self.covariance_matrix[left_index][left_index] +  self.covariance_matrix[right_index][right_index]
        
    def marginalize(self, index):
        return (self.mean_vector[index], self.covariance_matrix[index][index])


    def condition(self, val, index_rv_obs, index):
        #Update mean vector
        old_mean = self.mean_vector[:index_rv_obs]
        #print(old_mean)
        var_of_obs = self.covariance_matrix[index_rv_obs][index_rv_obs]
        mean_of_obs = self.mean_vector[index_rv_obs]
        covariance_vector_of_obs = self.covariance_matrix[index_rv_obs, 0:index_rv_obs]
        self.mean_vector = old_mean + ((val - mean_of_obs) / var_of_obs) * covariance_vector_of_obs

        #Update covariance
        old_covariance = self.covariance_matrix[0:index_rv_obs,0:index_rv_obs]
        dim = covariance_vector_of_obs.size
        dot_prod = covariance_vector_of_obs.reshape(dim,1).dot(covariance_vector_of_obs.reshape(1,dim))

        self.covariance_matrix = old_covariance.T - (1/var_of_obs * dot_prod)
