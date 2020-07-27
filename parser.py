import csv
import os

def data_parser(data):
        new = ""
        lines = data.split("\n")
        for line in lines:
            if line == "":
                continue
            if line[0] == '+':
                if len(line) > 2 and line[1] == '+':
                    # print(line)
                    path = line[6:]
                    new += path + '\n'
                else:
                    # print(line)
                    change = line[1:]
                    change = change.strip()
                    # print(new)
                    new += change + '\n'
        print(new)
        return new

def mkdir(name):
		try:
			# If file is not exist
			if not(os.path.isdir(name)):
				os.makedirs(os.path.join(name))
		except Exception as e:
			print("[Make Error] : %s." %e)

def run():
    csv_f = None # null object

    try:
        csv_f = open('real_csv.csv','r') # Open csv file
    except FileNotFoundError as e:
        print("FileNotFound! Check your file path and try again")

    rdr = csv.reader(csv_f) # Get text
    mkdir("MappingCommitFiles")

    org_path = os.getcwd()
    set_path = org_path + "/MappingCommitFiles"
    os.chdir(set_path)

    
    for line in rdr:
        filename = line[1]
        data = line[5]
        if(filename == "d803f0c2188c679de3dacf10741005b217425a33"):
            fd = open(filename + ".txt", 'w')
            new_data = data_parser(data)

    fd.write(new_data)
    fd.close()
        
    os.chdir(org_path)
