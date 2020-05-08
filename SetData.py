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

    path_dir = "C:/Lab/EJTool/Ngram/data/MappingCommitFiles"
    
    file_list = os.listdir(path_dir) # Save file list in MappingCommitFiles

    filename = input("Input a filename that include url information : ")

    cnt = 0
    file_dict = dict()
    file_hash = []

    csv_f = open('sample.csv','r') # Open csv file

    rdr = csv.reader(csv_f) # Get text 

    for line in rdr:
        # It is a variable that used to ignore the first line of csv file
        if cnt > 0: 
            # Separate file extension    
            re_line = line[2].split(".") 
            file_hash.append(re_line[0])
            # Hash value and path mapping
            file_dict[line[2]] = line[5] 
        cnt += 1

    return filename, file_hash, file_dict, file_list
