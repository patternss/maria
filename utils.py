#utils.py

import os
import shutil
import tempfile
import subprocess

def backup_file(file_path):
    if os.path.exists(file_path):
        backup_path = f'{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak'
        shutil.copy(file_path, backup_path)
        

def save_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)


#excluded should be a list or a tuple        
def to_dict(obj, excluded):
    return {key: value for key, value in obj.__dict__.items() if key not in excluded}


#a function that let's the user eidit something 
#in an editor. Can take text data and initialize the 
#opened file with that. Returns the text data that
#was created/edited in the editor
def open_editor(*,text_data=None):
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
        

