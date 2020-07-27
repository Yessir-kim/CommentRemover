# from pydriller import *
from git import *
import os
import shutil
import stat
import csv
import re
import subprocess
import SetData as sd
import parser as pa

pa.run()

filename, file_dict, file_hash =  sd.InitData()

cnt = 0

# File is cloned based on url.
with open(filename,'r') as txtinput:
    all_lines = txtinput.readlines()
    all_num = len(all_lines)
    
    for url_data in all_lines:
        cnt += 1
        try:
            if cnt == all_num:
                Git('clone_data').clone(url_data)
            else:
                url_data = url_data[:len(url_data) - 1]
                Git('clone_data').clone(url_data)
        except Exception as e:
            print("Alerady exist")
        origin = url_data.split("/")
        or_name = origin[len(origin) - 1]
# -------------------------------------------------------------------------------------------------------
        org_path = os.getcwd()
        set_path = org_path + "/clone_data/" + or_name

        for i in range(len(file_hash)):
            os.chdir(set_path)
        	# Get file data that is the full sorce code
            cmd_show = 'git show ' + str(file_hash[i]) + ':' + str(file_dict[file_hash[i]])

            data = subprocess.check_output(cmd_show, shell=True)

            data = data.decode('utf-8')

            # Regular expression to remove comment in the full source code
            data = re.sub(re.compile('\s//.*?\n|/\*.*?\*/',re.DOTALL ) ,"" ,data)
                
            # Get file data that is specific commit file    
            match = open(org_path + "/MappingCommitFiles/"+file_hash[i]+".txt").readlines()

            tmp_line = "" # It is a variable that save the code for a commit file

            # Check loop
            for line_words in match:
                # If a specific code(that is, line_words) is in data that is the full source code
                line_words = line_words.strip()
                # print(line_words)
                if line_words in data: 
                    tmp_line += line_words + "\n" # This line is not a comment. So save the code in tmp_line
                                
            # If tmp_line is empty, then it is a file included only comment lines
            if tmp_line == "": 
                # This file is an unnecessary file, so it is deleted from the directory.
                os.remove(org_path + "/MappingCommitFiles/"+file_hash[i]+".txt") 
            # At least it means that there is a line, not a comment
            else:
                # Overwriting process
                fdm = open(org_path + "/MappingCommitFiles/"+file_hash[i]+".txt", 'w+')
                fdm.write(tmp_line)
                fdm.close()

        os.chdir(org_path)
