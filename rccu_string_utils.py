import bpy
import os

'''
    Utilities for string operations specific to the rigify custom constraints utility.
'''

# string to bool --------------------------------------------------------
def str_to_bool(string):
    '''
        returns true/false based on string.
    '''
    if string == 'True':
        return True
    if string == 'False':
        return False
# ----------------------------------------------------------------------

# make_directory_string -------------------------------------------------
def make_directory_string(armature):
    '''
        makes a directory string based on the armature name, 
        creating folder/files if none exist.
    '''
    
    # make a folder if none exists.
    print(f">make_directory_string for armature \"{armature.name}\"")
    #make a folder -------------------------------------------
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    # make path string from armature name and suffix.
    newpath = os.path.join( directory , armature.name+'_constraintlink')
    # create a folder if one doens't exist already:
    if not os.path.exists(newpath):
        print(f">created folder for {armature.name}")
        os.makedirs(newpath)
    # use armature name for file name.
    fileName = f"{armature.name}.txt"
    return newpath+"\\"+fileName
# ----------------------------------------------------------------------

# extract name from pointer string -------------------------------------
def extract_name_from_pointer_string(pointer_string):
    '''
        gets the name from a bpy pointer as string.    
    '''
    split = pointer_string.split('\"')
    found_name = ''
    for item in split:
        print(item)
        if '<' not in item and '>' not in item:
            found_name = item
            return found_name
    return ''
# ----------------------------------------------------------------------

# EXTRACT THE NAME FROM A DATA PATH ----------------------------------------
def extract_name_from_data_path(base_string, sub_string):
    # try to find the string:
    try:
        sub_start = base_string.index(sub_string)
    except:
        return ''
    #
    base_string_len = len(base_string)
    # remove the beginning of the string.
    string_begin = base_string[:-(base_string_len - sub_start)]
    name = base_string.replace(string_begin, '')
    
    
    # find bracket position
    bracket_start = name.index('[')
    bracket_end   = name.index(']')
    # remove what's at the end of the bracket.
    name = name[:-(len(name)-bracket_end-1)]
    # remove the sub string.
    name = name.replace(sub_string, '')
    # remove brackets
    name = name[1: ]
    name = name[ :-1]
    # remove quotes
    name = name[1: ]
    name = name[ :-1]
    
    print('final name: '+name)
    return str(name)
# --------------------------------------------------------------------------