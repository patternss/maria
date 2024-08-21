import sys
import os

from maria import Maria
from cli import CLI
from collection import Collection

UI_names = ['CLI', 'QT']

#create and load collection:
collection_name = 'default'

#check if database file exists:
if not os.path.exists(f'{collection_name}_col.json'):
    print('path did not exist')
    #create an empty file if it doesn't exist
    with open(f'{collection_name}_col.json', 'w') as json_file:
        json_file.write('{}')
default_collection = Collection(collection_name)



#choose the UI based on the command line arguments
UI_name = 'CLI' #default UI
if len(sys.argv) > 1: #if command line arguments have been passed:
    if sys.argv[1] in UI_names:
        UI_name = sys.argv[1]
    else:
        sys.exit('Failed to provide acceptable command line argument for UI')


match UI_name:
    case 'CLI':
        UI = CLI()
                
    case 'QT':
        pass
                
maria = Maria(collection = default_collection, UI=UI)
maria.session()

