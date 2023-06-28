# Gauss Privug

Proof of concept implementation of a Privug backend featuring an exact Bayesian inference engine based on multivariate Gaussian distributions.

# Content of the repository

This repository accompanies the paper "Exact and Efficient Bayesian Inference for Privacy Risk Quantification".

This repository contains the public statistics release case study and the benchmarks for the scalability evaluation of the inference engine. The examples can be executed in the notebook `eval.ipynb`. The folder `case_study_files` contains the files for the case study. The scalability folder `scalability_files` contains the template programs for the scalability evaluation. The evaluation functions in `utils/eval.py` instantiate the benchmark programs with increasing number of variables.
