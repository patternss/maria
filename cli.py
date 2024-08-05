#Command line interface for Maria
#Responsibilities: takes user input and displays answers to the user.
#sends the user prompts to Maria and receives the answers from her.


class CLI():
    def __init__(self ):
        pass

    def ask_input(self, message):
        return input('- ' + message + '\n>>>')

    def provide_output(self, message):
        print('- ' + message)


