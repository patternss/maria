#Command line interface for Maria

from problem import Problem
from maria import Maria

#initialization 
maria_1 = Maria('problems.txt')

#command line loop
cmnd = ''
quit_cmnds = ['quit', 'q', 'exit'] 
while cmnd not in quit_cmnds:
   cmnd = input('>>>')
   match cmnd:
        case 'c': #create a new problem
            description = input('Input the description for the problem:\n>>>')
            thing = input('Input the thing (entity, object, article, phenomenon, pattern):\n>>>')
            topic = input('Input the topic for the new problem:\n>>>')

            maria_1.create_problem(topic, description, thing )
            
        case 'p': #present the user with a new problem
            problem = maria_1.present_problem()
            print(problem.description)

#exit
