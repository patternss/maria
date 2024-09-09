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

