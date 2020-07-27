# Set Data that is commit files and csv file
import os
import csv

def InitData():
    # Make a clone data folder
    try:
        # If file is not exist 
        if not(os.path.isdir('clone_data')): 
            os.makedirs(os.path.join('clone_data'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            # Ignore exception
            print("Alerady exist") 

    filename = input("Input a filename that include url information : ")

    org_path = os.getcwd()

    path_dir = org_path + "/MappingCommitFiles"
    
    file_list = os.listdir(path_dir) # Save file list in MappingCommitFiles

    file_dict = dict()
    path = ""
    file_hash = []
    
    os.chdir(path_dir)
    
    for name in file_list:
        with open(name, 'r') as hFile:
            all_lines = hFile.readlines()
            print(all_lines)
            hName = name.split(".") # hash value
            path = all_lines[0]
            file_hash.append(hName[0])
            file_dict[hName[0]] = path
    
    os.chdir(org_path)
    
    return filename, file_dict, file_hash
