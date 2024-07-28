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
        
        
       # case 't': #choose a topic for presented problems
         #   topic = input('Input topic name (empty or "all" will include all topics):\n>>>')
          #  if maria_1.set_topic(topic):
           #     print(f'Topic was set to topic)
        

        case 'h': #show possible commands to the user
            print('Available actions:\nc: create a new problem\np: present a problem\nq, quit, exit: exit the learning session')
        
        case _:
            print('Unknown command, please try again or type "h" to see help with commands')

#exit
