#maria.py - A module that implements Maria, a learning assistant. 
#maria is responsible for processing user input, serving the UI with problems
#and error codes and information. Maria also receives problems from the 
#collection and chooses a suitable problem for the user.
import random
import heapq
import datetime
from collections import defaultdict

from problem import Problem
from pattern import Pattern

class Maria():

    def __init__(self, collection=None, UI=None):
        self.collection = collection 
        self.UI = UI
        self.act_problems = []
        self.act_topic_groups = []
        self.topic_prominences = defaultdict(int) 
        self.min_prominence = 1.15
        self.commands = {
                'help' : self.help,
                'h'    : self.help,
                'problem' : self.problem,  
                'p'       : self.problem,
                'quit' : self.shutdown,           
                'q'    : self.shutdown,
            }

    #starts a interaction loop with Maria
    def session(self):
        while True:
            command = self.UI.ask_input('What do you want to do next?').split()

            if command[0] not in self.commands.keys():
                self.UI.provide_output('''Incorrect input, please try again \
or type "help" for more information''')

            else:
                self.commands[command[0]](command)
            if command[0] in ['quit', 'q']:
                #save currently used collection to database
                self.collection.close_collection()
                break

    #prints helpful information about available commands
    def help(self, command):
        self.UI.provide_output('''Here are the available commands \n:
    problem (p): provide a new active problem if such can be found.
        subcommands for problem:
            create (c): create a new problem.
            delete (d): delete problem(s) with given id(s). Ex. p delete 12
            edit   (e): edit an existing problem. Ex. p edit 15  

    help (h): Shows information about the commands
    quit (q): Quits the current session
    ''')

    #processed the problem command and its possible arguments
    def problem(self, command):
        if len(command) == 1: #only 'problem' or 'p' was given
            self.provide_problem()
        
        else: #additional command arguments: 
            match command[1].upper():
                case 'C' | 'CREATE':
                    self.create_problem()

                case 'D' | 'DELETE':
                    self.delete_problem(command[2]) #id to be deleted 

                case 'E' | 'EDIT':

                    #if problem sections were given:
                    if len(command) > 3:
                        self.edit_problem(int(command[2]), command[3:])
                    else:
                        self.edit_problem(int(command[2])) #id of the to be edited problem

                case 'I' | 'INFO':
                    if len(command) == 2: #no problem id given
                        prob_info = self.collection.get_problem_info()
                    else: #problem id given - only one id shoud be passed here
                        prob_info = self.collection.get_problem_info(int(command[2]))
                        if not prob_info: #id was not found
                            self.UI.provide_output(\
                                    f'Could not found a problem with given id')
                            return

                    for piece in prob_info:
                        self.UI.provide_output(piece)

                case _ :
                    self.UI.provide_output('Unknown argument for command "create".')



    #closes the session and calls collection to save its data
    def shutdown(self, command):
        self.UI.provide_output('Goodbye!')

    #takes input for a new problem and passes it to database(s),
    #when inverse is True, another problem is also created 
    #swiching the order of the patterns
    def create_problem(self): 
        instructions = {
                'pat_1': 'Provide the first pattern:', 
                'pat_2': 'Provide the second pattern:',
                'topics':'Please provide topics for the problem',
                'two_way': 'Do you want to create two-way problems? (y or n)'
                }
        inputs = {
                'pat_1':  None,
                'pat_2':  None,
                'topics': None,
                'two_way':None
                }

        keys = list(inputs.keys())
        index = 0

        while index < len(keys):
            key = keys[index]
            usr_input = self.UI.ask_input(instructions[key])

            #check for abort and editor commands:
            if usr_input.upper() in ['%A', '%ABORT']:
                return #leave funciton without saving the new pattern
            elif any(word for word in usr_input.upper().split() if word\
                    in ['%E', '%EDIT', '%EDITOR']):
                usr_input = self.UI.open_editor(text_data=f'#{instructions[key]}\n\
{usr_input.replace("%e", "")}') 
                usr_input = usr_input.replace(f'#{instructions[key]}', '').strip()
                self.UI.provide_output(usr_input, source='user')

            inputs[keys[index]] = usr_input
            #if input is "two_way" and if feasible input was given 
            if not (keys[index] == 'two_way' and inputs[key].upper() not in\
                    ['Y', 'YES', 'N', 'NO']):
                    index += 1

        pat_1 = Pattern(inputs['pat_1'])
        pat_2 = Pattern(inputs['pat_2'])
        topics = inputs['topics'].split()

        prob_id = self.collection.add_problem(topics, pat_1, pat_2, save=True)
        if prob_id != None:
            self.UI.provide_output(f'Problem {prob_id} succesfully created.')
        if inputs['two_way'].upper() in ['Y', 'YES']:
            prob_id = self.collection.add_problem(topics, pat_2, pat_1, save=True)
            if prob_id != None:
                self.UI.provide_output(f'Problem {prob_id} succesfully created.')

        
    #provides a problem to chosen client by fetching new problems, if the
    #there are no active problems. defines a prob_filter function that 
    #implements the intelligence to filter wanted problems. chooses the 
    #next question based on previous context and a bit of randomness
    def provide_problem(self):
        #if there are no active problems left:
        if not self.act_problems:

            #filtering func for choosing which problems are chosen from a collection
            def prob_filter(probs, count = 3, min_prom = 1.15):
                selected = heapq.nlargest(count, probs.values(),\
                        key=lambda prob: prob.prominence) #nlargest returns n or the
                                                            #max number found
                #return problems that are above a minimum prominence value 
                return [prob for prob in selected if prob.prominence > min_prom]

            #get problems from the collection: 
            filtered_probs = self.collection.get_problems(self.act_topic_groups,\
                    prob_filter)

            self.act_problems = filtered_probs 

            #if no matching problems were found:
            if not self.act_problems:
                self.UI.provide_output('There are no active problems at the \
moment. Good job!')
                return 
        
        #choose on problem randomly:
        prob = random.choice(self.act_problems)

        #create message about the chosen problem
        problem_prompt = f'Problem id: {prob.prob_id} -\
 Topics: {", ".join(prob.topics)}\n\n{prob.pat_1.content}\n' 

        #send the problem to the user
        self.UI.provide_output(problem_prompt)

        #ask for an answer:
        answ = self.UI.ask_input("Give your answer or hit 'enter'.")
        #check if user wants to use editor:
        if [word for word in answ.strip().upper().split() if word\
                in ['%E', '%EDIT', '%EDITOR']]:
            #open editor with problem promt and user input discarding %e and removing
            #problem promt at the end
            answ = self.UI.open_editor(text_data=\
                    f'**{problem_prompt}**\n{answ.replace("%e", "")}').replace(\
                    f'**{problem_prompt}**', '')
            self.UI.provide_output(answ, source='user')
        self.UI.provide_output(f'Here is the matching pattern:\n\n {prob.pat_2.content}\n')

        #ask for answer rating
        rating = None
        while rating not in ['C','I']:
            rating = self.UI.ask_input("How did it go? rate the answer - c for correct and i for incorrect").upper()
            if rating == 'C':
                prob.ratings.append(1)
                prob.time_answ_cor = datetime.datetime.now()
                
            else:
                prob.ratings.append(0)
        
        #update the mastery lvl and update the problem in the collection
        prob.calc_mast_lvl()
        self.collection.replace_problem(prob)
        
        #self.update_topic_proms(prob) 

        #remove the problem from actives
        self.act_problems.remove(prob)


    def delete_problem(self, prob_id):
            if self.collection.delete_problem(int(prob_id)):
                self.UI.provide_output(f'problem {prob_id} deleted.')
            else:
                self.UI.provide_output(f"Failed to delete problem with\
given id ({prob_id}). Id doesn't exist. ")

    
    #updates an excisting problem, 
    def edit_problem(self, prob_id, sections = ['P1', 'P2', 'TOPICS']):
        #uppercase the problems sections:
        sections = [section.upper() for section in sections]
        #get the problem matching the id:
        problem = self.collection.get_problem_by_id(prob_id)
        #if problem does not exist:
        if not problem:
            self.UI.provide_output(f'Could not find a problem with given id')
            return

        #edit chosen sections
        for section in sections:
            match section:
                case 'P1' : 
                    problem.pat_1.content = self.UI.open_editor(text_data =\
                            problem.pat_1.content)
                case 'P2' :
                    problem.pat_2.content = self.UI.open_editor(text_data =\
                            problem.pat_2.content)
                case 'TOPICS' :  problem.topics = self.UI.open_editor\
                        (text_data=' '.join(problem.topics)).split()
                case _ : 
                    self.UI.provide_output(f'{section} is not a proper\
 argument. Discarding all edits.')
                    return False

        #replace the original problem with the edited one
        self.collection.replace_problem(problem)
        self.UI.provide_output(f'Problem {prob_id} successfully edited.')
    
    #update the topic prominences
    def update_topic_proms(self, prob, decay=0.7):
        #aply decay to all existing act topics:
        for topic in self.topic_prominences:
            self.topic_prominences[topic] *= decay
         
        #add prominence if it was a topic of the previous question:
        for topic in prob.topics:
            self.topic_prominences[topic] += 1
            
    #add new topic groups to the active_topic_gr{oups:
    def add_topic_groups(topic_groups):
        pass

    #remove excisting topic groups from the active topic groups
    def remove_topic_groups(topic_groups):
        pass

    #clear all topics from the active_topic_groups
    def clear_topics():
        pass

