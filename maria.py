#maria.py - A module that implements Maria, a learning assistant. 
#maria is responsible for processing user input, serving the UI with problems
#and error codes and information. Maria also receives problems from the 
#collection and chooses a suitable problem for the user.
import random
import heapq
import datetime

from problem import Problem
from pattern import Pattern

class Maria():

    def __init__(self, collection=None, UI=None):
        self.collection = collection 
        self.UI = UI
        self.act_problems = []
        self.act_topic_groups = []
        self.commands = {
                
                'create' : self.create_problem,
                'help' : self.help,
                'problem' : self.provide_problem,  
                'quit' : self.shutdown,           
                'pinfo' : self.collection.print_prob_info
    
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
                #save currently used collection to database
                self.collection.close_collection()
                
                break

    #takes input for a new problem and passes it to database(s),
    #when inverse is True, another problem is also created 
    #swiching the order of the patterns
    def create_problem(self, inverse=True): 
        topics = self.UI.ask_input('Please provide topics for the problem.')
        pat_1 = self.UI.ask_input('Provide the first pattern:')
        pat_2 = self.UI.ask_input('Provide the second pattern:')

        pat_1 = Pattern(pat_1)
        pat_2 = Pattern(pat_2)

        self.collection.add_problem(topics, pat_1, pat_2)
        if inverse:
            self.collection.add_problem(topics, pat_2, pat_1)

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
        #if there are no active problems left:
        if not self.act_problems:

            #filtering func for choosing which problems are chosen from a collection
            def prob_filter(probs, count = 1, min_prom = 1):
                selected = heapq.nlargest(count, probs.values(),\
                        key=lambda prob: prob.prominance) #nlargest returns n or the
                                                            #max number found
                #return problems that are above a minimum prominance value 
                return [prob for prob in probs.values() if prob.prominance > min_prom]

            #get problems from dictionary 
            self.act_problems = self.collection.get_problems(self.act_topic_groups,\
                    prob_filter)
            

            #if no matching problems were found:
            if not self.act_problems:
                self.UI.provide_output('''No matching problems were found with \
                        current topic groups. Try changing them or add problems.''')
                return 
        
        #choose which problem to present next:
        prob = self.act_problems.pop(0)
        #send the problem to the user
        self.UI.provide_output(f'''Here is a problem for you:\n\n \
{prob.pat_1.content}\n''')

        #ask for an answer
        answ = self.UI.ask_input("Give your answer (or hit enter if not feasible")
        self.UI.provide_output(f'Here is the matching pattern:\n\n {prob.pat_2.content}\n')

        #ask for problem rating
        rating = None
        while rating not in ['C','I']:
            rating = self.UI.ask_input("How did it go? rate the problem - C for correct and I for incorrect").capitalize()
            if rating == 'C':
                prob.ratings.append(1)
                prob.time_answ_cor = datetime.datetime.now()
                
            else:
                prob.ratings.append(0)
        
        prob.calc_mast_lvl()
        self.collection.replace_problem(prob)
    

    #updates an excisting problem
    def update_problem(self, prob_id):
        pass
    
    
    #add new topic groups to the active_topic_groups:
    def add_topic_groups(topic_groups):
        pass

    #remove excisting topic groups from the active topic groups
    def remove_topic_groups(topic_groups):
        pass

    #clear all topics from the active_topic_groups
    def clear_topics():
        pass
    #closes the session and calls collection to save its data
    def shutdown(self):
        self.UI.provide_output('Goodbye!')
