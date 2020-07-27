import os
import csv
import shutil

# mkae a dir or remove a dir 

class SetInfo:
		def __init__(self):
				self.path = os.path 
		
		def mkdir(self):
			try:
				# If file is not exist
				if not(self.path.isdir('hash_data')):
					os.makedirs(self.path.join('hash_data'))
			except Exception as e:
				print("[Make Error] : %s." %e)

		def remove_readonly(self, func, path, excinfo):
			os.chmod(path, stat.S_IWRITE)
			func(path)
		
		def rmdir(self, remove_dir):
			try:
				shutil.rmtree(remove_dir, ignore_errors=False, onerror=self.remove_readonly)
			except PermissionError as e:
				print("[Delete Error] %s - %s." % (e.filename,e.strerror))
