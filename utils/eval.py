import time
from importlib import reload
import src as exact_inference
from subprocess import call
import pymc as pm

SYNTH1_TEMPLATE_GAUSS   = './scalability_files/eval_scale.py.template'
SYNTH1_TEMPLATE_PSI     = './scalability_files/eval_psi_scale.psi.template'
SYNTH2_TEMPLATE_GAUSS   = './scalability_files/eval_scale_cond.py.template'

def time_gauss(size,template):
    reload(exact_inference.parser)
    reload(exact_inference.evaluator)
    target_file = prepare_file(size,template)
    t_init = time.time()
    program: List[exact_inference.Statement] = exact_inference.parse(target_file)
    posterior_marginal: exact_inference.distribution = exact_inference.evaluate(program)
    total_time = time.time() - t_init
    print(f'Privug exact | Size {size} | Time {total_time}')
    return total_time

def time_psi(size,template):
    target_file = prepare_file(size,template)
    t_init = time.time()
    call(['psi', target_file])  # TODO: redirect STDOUT
    total_time = time.time() - t_init
    print(f'PSI | Size {size} | Time {total_time}')
    return total_time    

def time_privug_nuts(size):
    t_init = time.time()
    # ---- PyMC model for the experiment ----
    with pm.Model() as model:
        x = pm.Normal('x', 1,1, shape=size)
        sum_ = pm.Deterministic('sum', pm.math.sum(x))
        posterior = pm.sample(draws=10_000, chains=2)
    # ---- PyMC model for the experiment ----
    total_time = time.time() - t_init
    print(f'Privug NUTS | Size {size} | Time {total_time}')
    return total_time

def prepare_file(size,path_template):
    """
    Function to prepare instantiate the evaluation templates
    """
    
    output_file   = path_template.split('.template')[0]
    with open(path_template, 'r') as file:
      filedata = file.read()
    
    # Replace the target string
    filedata = filedata.replace('{{size}}', str(size))
    
    # Write the file out again
    with open(output_file, 'w') as file:
      file.write(filedata)

    # return a string pointing to the generated file
    return output_file