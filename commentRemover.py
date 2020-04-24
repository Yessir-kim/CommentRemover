from git import *
import os
import shutil
import stat
import csv
import re
import subprocess
# -------------------------------------------------------------------------------------------------------
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)
    
def remove_dir_tree(remove_dir):
    try:
        shutil.rmtree(remove_dir, ignore_errors=False, onerror=remove_readonly)
    except(PermissionError) as e:
        print("[Delete Error] %s - %s." % (e.filename,e.strerror))
# -------------------------------------------------------------------------------------------------------
# Make a clone data folder
try:
    # If file is not exist 
    if not(os.path.isdir('clone_data')): 
        os.makedirs(os.path.join('clone_data'))
except OSError as e:
    if e.errno != errno.EEXIST:
        # Ignore exception
        print("Alerady exist") 

"""
    이 부분을 바꿔야 함. 주석을 제거하는 기준은 MappingCommitFiles가 아닌 csv file임 - 일단 보류

    1. csv file에서 +로 시작하는 부분을 따로 추출해야 함 (이게 곧 Mapping folder에 있는 file이기 때문)
    2. 이때 파일을 바로 만드는게 아니라 comment인지 확인 후 만드는게 더 효율적으로 보임

"""

# -------------------------------------------------------------------------------------------------------
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

cnt = 0 # Reuse

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
            if file_hash[i]+".txt" in file_list:
                os.chdir(set_path)

                # Get file data that is the full sorce code
                cmd_show = 'git show ' + str(file_hash[i]) + ':' + str(file_dict[file_hash[i]])

                data = subprocess.check_output(cmd_show, shell=True)

                data = data.decode('utf-8')

                # Regular expression to remove comment in the full source code
                data = re.sub(re.compile('\s//.*?\n|/\*.*?\*/',re.DOTALL ) ,"" ,data)
                
                """
                if file_hash[i]+".txt" in file_list:
                    # Get file data that is the full sorce code
                    data = open("clone_data/httpcomponents-client/"+file_dict[file_hash[i]]).read()
                        
                    # If it is code before removing comments
                    if not file_hash[i] in che_table:
                        # Regular expression to remove comment in the full source code
                        data = re.sub(re.compile('\s//.*?\n|/\*.*?\*/',re.DOTALL ) ,"" ,data) # 주석제거 보충완료
                        # Overwriting process that prevent to duplication
                        fd = open("clone_data/httpcomponents-client/"+file_dict[file_hash[0]], 'w+')
                        fd.write(data)
                        fd.close()

                """
                # Get file data that is specific commit file    
                match = open("C:/Lab/EJTool/Ngram/data/MappingCommitFiles/"+file_hash[i]+".txt").readlines()

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
                    print("This txt_file is comment")

                    # This file is an unnecessary file, so it is deleted from the directory.
                    os.remove("C:/Lab/EJTool/Ngram/data/MappingCommitFiles/"+file_hash[i]+".txt") 
                # At least it means that there is a line, not a comment
                else:
                    # Overwriting process
                    fdm = open("C:/Lab/EJTool/Ngram/data/MappingCommitFiles/"+file_hash[i]+".txt", 'w+')
                    fdm.write(tmp_line)
                    fdm.close()

            os.chdir(org_path)
                
        # remove_dir_tree('clone_data\\' + or_name)
        
    # remove_dir_tree('clone_data')
