from request import request
from json import loads
from subprocess import call

files_data = loads(request("http://localhost:8080/file/", "GET")[1])
files_count = len(files_data)
for i in range(files_count):
  file = open('src/' + files_data[i]["fileName"], 'w')
  file.write(files_data[i]["fileData"])
  file.close()

call('python src/main.py', shell=True)