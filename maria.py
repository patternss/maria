#maria.py - A module that implements Maria, a learning assistant. 
#maria is responsible for processing user input, serving the UI with problems
#and error codes and information. Maria also receives problems from the 
#collection and chooses a suitable problem for the user.

from problem import Problem

class Maria():

    def __init__(self, collection=None, UI=None):
        self.collection = collection 
        self.UI = UI
        
        self.commands = {
                
                'create' : self.create_problem,
                'help' : self.help,
                'problem' : self.problem,  
                'quit' : self.shutdown,            
    
            }


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

    #creates a new problem and saves it to database(s)
    def create_problem(self, topic, description, thing):
        pass

    def help(self):
        self.UI.provide_output('''Here are the available commands:
        create - Creates a new problem
        help - Shows information about the commands
        problem - Ask Maria for a new problem
        quit - Quits the current session
    ''')

    def shutdown(self):
        self.UI.provide_output('Goodbye!')

    #gives a new problem to chosen client
    def problem(self):
        #choose which problem to present next:
        pass 

    def update_problem(self):
        pass
    

