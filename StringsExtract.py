import os
import re
import json
pattern = re.compile("\"(?:\\\.|[^\"\\\])*\"")

def find(dir):
	for dirfile in os.listdir(dir):
		path = os.path.join(dir, dirfile)
		if (os.path.isfile(path) and not (path.endswith("strings.json"))):
			print("Searching "+path)
			try: 
				with (open(path, mode="r", encoding="utf-8") as f):
					lines = f.readlines()
					linen = 0
					for line in lines:
						searchs = pattern.finditer(line)
						found = False
						num = 0
						for search in searchs:
							found = True
							string = search.group().replace("\"","")
							print(f"Found {string} in {path} at line {linen}, num {num}")
							strings[path.replace(directory,"").lstrip("\\")+":"+str(linen)+":"+str(num)] = string
							num += 1
						linen += 1
					if (found):
						print(f"No string was found in {path}")
			except:
				print("Error encountered when loading "+path)
		elif (os.path.isdir(path)):
			find(path)

def output(dir):
	with open(dir+"/strings.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(strings, indent=4, separators=(',', ': ')))

def inputt(jsonf):
	global strings
	with open(jsonf+"/strings.json", mode="r", encoding="utf-8") as f:
		print(jsonf+"/strings.json")
		strings = json.loads(f.read())

def write(dir):
	dir+="/"
	for file in strings.keys():
		key = file.split(":")
		path = key[0].replace("\\","/")
		linen = int(key[1])
		num = int(key[2])
		print("Writing "+strings[file]+" into "+path+" at line "+str(linen)+", num "+str(num))
		os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
		cont = None
		m = "r+"
		if (not os.path.exists(dir+"Repacked/"+path)):
			m = "w+"
			try:
				with (open(dir+path, mode="r", encoding="utf-8") as f):
					cont = f.readlines()
			except:
				print("Error encountered when loading "+dir+path)
		try:
			with (open(dir+"Repacked/"+path, mode=m, encoding="utf-8") as ff):
				if (cont == None):
					lines = ff.readlines()
				else:
					ff.writelines(cont)
					lines = cont
				ff.seek(0)
				line = lines[linen]
				searchs = pattern.findall(line)
				if (len(searchs) != 0):
					line.replace(searchs[num],"\""+strings[file]+"\"",1)
					lines[linen] = line
				else:
					print(f"No string was found in {path}")
				ff.writelines(lines)
		except:
			print("Error encountered when loading "+dir+"Repacked/"+path)

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