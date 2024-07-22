#Command line version of Maria

import sys
from problem import Problem

#initialization 
# data structure for storing the problems
problems = []

# load information
file_path = 'problems.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# import the problems into the problems data structure
for line in lines:
    prob_components = line.split('|')
    new_problem = Problem(prob_components[0], prob_components[1])
    problems.append(new_problem)



#command line loop
cmnd = ''
quit_cmnds = ['quit', 'q', 'exit'] 
while cmnd not in quit_cmnds:
    match cmnd:
        case 

#exit
