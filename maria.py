#maria.py - A module that implements Maria, the virtual teacher. 
import random
from problem import Problem

class Maria():

    def __init__(self, problems_db):
        self.problems_db = problems_db
        self.problems = {}
        #initialize the datastructure from the database:
        
        #check db type later here

        with open(problems_db, 'r') as file:
            lines = file.readlines()

        for line in lines:
            #TRY EXCEPT???
            components = line.split('|')
            new_prob = Problem(int(components[0]), components[1], components[2], components[3])
            self.problems[new_prob.id] = new_prob

    #creates a new problem and saves it to database(s)
    def create_problem(self, topic, description, thing):
        next_id = max(self.problems) + 1
        #create new problem
        new_problem = Problem(next_id, topic, description, thing)
        #add new problem to datastructure
        self.problems[next_id] = new_problem
        #add new problem to the database:
        with open (self.problems_db, 'a') as file:
            file.write(f'{next_id}|{topic}|{description}|{thing}')

    #gives a new problem to chosen client
    def present_problem(self):
        #choose which problem to present next:
        return random.choice(list(self.problems.values()))
        
    def update_problem(self):
        pass
