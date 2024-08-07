#maria.py - A module that implements Maria, a learning assistant. 
#maria is responsible for processing user input, serving the UI with problems
#and error codes and information. Maria also receives problems from the 
#collection and chooses a suitable problem for the user.
import random

from problem import Problem
from pattern import Pattern

class Maria():

    def __init__(self, collection=None, UI=None):
        self.collection = collection 
        self.UI = UI
        self.act_topic_groups = []
        self.commands = {
                
                'create' : self.create_problem,
                'help' : self.help,
                'problem' : self.provide_problem,  
                'quit' : self.shutdown,            
    
            }

    #starts a interaction loop with Maria
    def session(self):
        while True:
            command = self.UI.ask_input('What do you want to do next?')
            if command not in self.commands.keys():
                self.UI.provide_output('''Incorrect input, please try again \
or type "help" for more information''')

            else:
                self.commands[command]()
            if command == 'quit':
                break

    #takes input for a new problem and passes it to database(s)
    def create_problem(self): 
        topics = self.UI.ask_input('Please provide topics for the problem.')
        pat_1 = self.UI.ask_input('Provide the first pattern:')
        pat_2 = self.UI.ask_input('Provide the second pattern:')

        self.collection.add_problem(topics, pat_1, pat_2)

    #prints helpful information about available commands
    def help(self):
        self.UI.provide_output('''Here are the available commands:
        create - Creates a new problem
        help - Shows information about the commands
        problem - Ask Maria for a problem to solve
        quit - Quits the current session
        topic add|remove|clear - add or remove topic (or topic group)\
                or clear all topics.
    ''')


    #provides a problem to chosen client
    def provide_problem(self):
         

        #get all the problems (copy) matching the function paramter 
        act_problems = self.collection.get_problems(self.act_topic_groups,\
                lambda probs : random.sample(probs.items(), 5) if len(probs) > 4\
                else random.sample(probs, len(probs)))
        

        #if no matching problems were found:
        if not act_problems:
            self.UI.provide_output('''No matching problems were found with \
                    current topic groups. Try changing them or add problems.''')
        else:
            #choose which problem to present next:
            rand_prob = random.choice(act_problems)[1] #!!!Random pick, change later!!!
            #send the problem to the user
            self.UI.provide_output(f'''Here is a problem for you:\n\n \
{rand_prob.pat_1.content}\n''')

            #ask for an answer
            self.UI.ask_input("Let me know when you are ready to see the answer by pressing enter")
            self.UI.provide_output(f'Here is the matching pattern:\n\n {rand_prob.pat_2.content}\n')

            #ask for problem rating
            rating = self.UI.ask_input("How did it go? rate the problem - C for correct and I for incorrect").capitalize()
            if rating == 'C':
                rand_prob.ratings.append(1)
            else:
                rand_prob.ratings.append(0)
        

    #updates an excisting problem
    def update_problem(self, prob_id):
        pass
    
    
    #add new topic groups to the active_topic_groups:
    def add_topic_groups(topic_groups):


    #remove excisting topic groups from the active topic groups
    def remove_topic_groups(topic_groups):
        pass

    #clear all topics from the active_topic_groups
    def clear_topics():

    #closes the session and calls collection to save its data
    def shutdown(self):
        self.UI.provide_output('Goodbye!')
