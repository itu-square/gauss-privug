from typing import List
from importlib import reload
import src.parser as parser
import src.evaluator as evaluator

def infer(path_to_program):
    reload(parser)
    reload(evaluator)
    
    program: List[parser.Statement] = parser.parse(path_to_program)
    posterior: evaluator.distribution = evaluator.evaluate(program)
    return posterior