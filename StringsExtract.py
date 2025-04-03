import os
import re
import json

def find(dir):
	for dirfile in os.listdir(dir):
		path = os.path.join(dir, dirfile)
		if (os.path.isfile(path) and not (path.endswith("strings.json"))):
			print("Searching "+path)
			with (open(path, mode="r", encoding="utf-8") as f):
				contents = f.read()
				search = re.search("\"(?:\\\.|[^\"\\\])*\"",contents)
				if (search):
					string = search.group().replace("\"","").replace("'''","")
					position = search.span()
					print(f"Found {string} in {path} at {position}")
					strings[path.replace(directory,"").lstrip("\\")+":"+str(position)] = string
				else:
					print(f"No string was not found in {path}")
				
		elif (os.path.isdir(path)):
			find(path)

def output(dir):
	with open(dir+"/strings.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(strings, sort_keys=True, indent=4, separators=(',', ': ')))

def inputt(jsonf):
	global strings
	with open(jsonf+"/strings.json", mode="r", encoding="utf-8") as f:
		print(jsonf+"/strings.json")
		strings = json.loads(f.read())

def write(dir):
	dir+="/"
	for file in strings.keys():
		path = file.split(":")[0].replace("\\","/")
		position = file.split(":")[1].replace("(","").replace(")","").split(", ")
		print("Writing "+strings[file]+" into "+path+" at "+str(position))
		with (open(dir+path, mode="r", encoding="utf-8") as f):
			cont = f.read()
		if (not os.path.exists(os.path.dirname(dir+"Repacked/"+path))):
			os.makedirs(os.path.dirname(dir+"Repacked/"+path))
		with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
			f.write(cont[:int(position[0])] + "\"" + strings[file] + "\"" + cont[int(position[1]):])

strings = {}
directory = input("Directory: ").replace("\\","/")
if (directory.endswith("/")):
	directory = dir[:-1]
inpt = input("Extract(e) / Repack(r)\nIf nothing input, found strings.json will repack, otherwise extract: ")
if (inpt == ""):
	if (os.path.exists(directory+"/strings.json")):
		print("strings.json was found in "+directory)
		inpt = "r"
	else:
		print("strings.json was not found in "+directory)
		inpt = "e"
if (inpt == "e" or inpt == "extract"):
	find(directory)
	output(directory)
elif (inpt == "r" or inpt == "repack"):
	inputt(directory)
	write(directory)
else:
	print("Invalid input")