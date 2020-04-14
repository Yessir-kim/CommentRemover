from pydriller import *
from git import *
import os
import shutil
import stat
import csv
import re

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)
    
def remove_dir_tree(remove_dir):
    try:
        shutil.rmtree(remove_dir, ignore_errors=False, onerror=remove_readonly)
    except(PermissionError) as e:
        print("[Delete Error] %s - %s." % (e.filename,e.strerror))

"""
1. url의 정보가 담긴 txt file을 받아서 readlines로 모든 줄을 받은 후 url 하나 하나를 clone해서 commit 정보를 추출 해냄
2. 근데 이렇게 하면 본인의 컴퓨터에 실제로 clone을 해야한다는 단점이 있다.

"""

try:
    if not(os.path.isdir('clone_data')): # 현재 py file이 있는 위치에 생성 
        os.makedirs(os.path.join('clone_data'))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Alerady exist") # Ignore exception

path_dir = "C:/EJTool/Ngram\data/MappingCommitFiles"
        
file_list = os.listdir(path_dir) # MappingCommitFiles에서 모든 파일 목록을 불러움 / 여기있는 파일이 곧 metric이기 때문에 여기 기준으로 검색해봐야 함

filename = input("Input a filename that include url information : ")
cnt = 0
file_dict = dict()
file_hash = []
tree = ""

csv_f = open('sample.csv','r')

rdr = csv.reader(csv_f)

for line in rdr:
    if cnt > 0:
        re_line = line[2].split(".") # 확장자 제외
        file_hash.append(re_line[0])
        file_dict[line[2]] = line[5] # Hash값이랑 path랑 mapping
    cnt += 1

# print(file_hash)
# print(file_dict)

cnt = 0
che_table = [0 for i in range(len(file_hash))]

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

        print("")

        # 이부분에 file_hash부분 for문 돌리면서 판단해야 함 
        for i in range(len(file_hash)):
            if file_hash[i]+".txt" in file_list:
                
                data = open("clone_data/ofbiz-framework/"+file_dict[file_hash[i]]).read()

                if che_table[i] != 1: # 즉, 해당 인덱스에 해당하는 파일을 열어보지 않았으면
                    data = re.sub(re.compile('//.*?\n|/\*.*?\*/',re.DOTALL ) ,"" ,data) # 주석제거 완료
                    fd = open("clone_data/ofbiz-framework/"+file_dict[file_hash[0]], 'w+') # 제거한 내용을 원래 파일에다가 덮어쓰기 - 일단 보류
                    fd.write(data)
                    
                match = open("C:/EJTool/Ngram\data/MappingCommitFiles/"+file_hash[i]+".txt").readlines()
                tmp_line = ""
                for line_words in match:
                    if line_words in data: # data안에 line이 있는 경우
                        tmp_line += line_words
                        print(line_words)

                if tmp_line == "": # tmp_line이 초기 설정값이랑 같다면 txt파일에 안에 있던 것들이 모두 주석이었다는 뜻
                    print("This txt_file is comment") # 모두 주석이였다면 mapping안에 파일은 삭제해도 된다는 것 -> 애초에 삭제하는 것이 좋을 
        
                che_table[i] = 1 # 읽었다는 것 표시
                
                # 이 부분에서 file_hash[].txt에 있는 code를 가져와서 전체를 비교해야하는데 한줄 한줄 비교한는게 나을 것 같은게 o
                # 만약에 전체를 한번에 통채로 비교한다면 comment랑 다른 comment가 아닌 code들이 한꺼번에 비교되기 때문에 어려움 o
                # 따라서 한줄 한줄 data안에 있는지 파악해야 할 것으로 보임 o
                # 만약 data안에 한 줄이 일치하면 주석이 아닌거고 없으면 주석임(주석은 이미 제거되었기 때문에) o

        """
        print(str(os.getcwd()) + '\\clone_data\\' + or_name)
        print("--------------------------------------------------------------------")
        for commit in RepositoryMining('clone_data\\' + or_name).traverse_commits(): # 해당 repos에 모든 commit 정보를 긁어 옴 (hash, code)
            for modification in commit.modifications:
                print('path{}'.format(modification.new_path))
                
            for modified_file in commit.modifications:
                code = modified_file.source_code
                try:
                    code = code.encode('unicode-escape').decode('utf-8')
                    # print(code) # code 출력 부분 (여기서 hash 값이 같으면 긁어오면 될 것 같음)
                except:
                    continue

            msg = commit.msg
            msg = msg.encode('unicode-escape').decode('utf-8')
            if "Fixed" in msg:
                print('apache,Fix,{},2020-04-03,human,'.format(commit.hash))
        """
        # remove_dir_tree('clone_data\\' + or_name)
        
    # remove_dir_tree('clone_data')

 
"""
        repo = Repo(str(os.getcwd()) + '\\clone_data\\' + or_name)
        
        commits_list = list(repo.iter_commits())
        for i in range(len(commits_list)):
            commit = commits_list[i]
            # print(type(commit.stats.files))
            for key, vlaue in commit.stats.files.items():
                print(key) # 현재 commit이 반영된 파일이름을 출력 
            author = repo.git.show("-s", "--format=Author: %an <%ae>", commit.hexsha)
            print(author) # commit 정보 출력
"""



"""
* 고려해야될 점
* 1. add_lines이기 때문에 현재 source code에 commit line이 존재하지 않을 수 있다.
     그래서 특정 commit을 볼 때 clone해서 찾는 방법을 써야되는데 효율적일까?
     -> checkout command를 사용하면 해결할 수 있을 것 같다.
     
* 2. python에 구현되어 있는 ast를 쓰면 python syntax기반으로 나온다.
     따라서 java ast를 위해서는 javalang을 사용해야 될 것으로 보인다. (사용법)
"""
