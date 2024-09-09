#Command line interface for Maria
#Responsibilities: takes user input and displays answers to the user.
#sends the user prompts to Maria and receives the answers from her.
import tempfile
import os
import subprocess

class CLI():
    def __init__(self ):
        pass

    def ask_input(self, message):
        return input('- ' + message + '\n>>>')

    def provide_output(self, message):
        print('- ' + message)


    #a function that let's the user eidit something 
    #in an editor. Can take text data and initialize the 
    #opened file with that. Returns the text data that
    #was created/edited in the editor
    def open_editor(self, *,text_data=None):
        #get the editor information from the system

        editor = os.environ.get('EDITOR')

        if not editor:
            if os.name == 'nt':
                editor = 'notepad'
            else:
                editor = 'nano'

        #create the tempfile and tempstream:
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='')\
                as temp_file:
            temp_file_path = temp_file.name

            if text_data:
                #add existing data to the temp file
                temp_file.write(text_data)
            #opend file with the editor
            temp_file.seek(0) #set the stream to beginning
            subprocess.run([editor, temp_file_path])
            #return data from the temp file:
            temp_file.seek(0) #set the stream to beginning
            return temp_file.read()
            

        
