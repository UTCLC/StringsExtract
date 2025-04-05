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
							string = search.group()[1:][:-1]
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
		f.write(json.dumps(strings, indent=4, separators=(',', ': '), ensure_ascii=False))

def inputt(jsonf):
	global strings
	with open(jsonf+"/strings.json", mode="r", encoding="utf-8") as f:
		strings = json.loads(f.read())

def write(dir):
	dir+="/"
	count = 0
	paths = {}
	for file in strings.keys():
		pathi = file.split(":")[0].replace("\\","/")
		if (pathi in paths.keys()):
			paths[pathi].append(count)
		else:
			paths[pathi] = [count]
		count += 1
	for path in paths.keys():
		os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
		lines = []
		try:
			with (open(dir+path, mode="r", encoding="utf-8") as f):
				lines = f.readlines()
		except:
			print("Error encountered when reading "+dir+path)
		try:
			ff = open(dir+"Repacked/"+path, mode="w", encoding="utf-8")
			for stringslinen in paths[path]:
				key = list(strings.keys())[stringslinen].split(":")
				linen = int(key[1])
				num = int(key[2])
				line = lines[linen]
				#print("Writing "+list(strings.values())[stringslinen]+" into "+path+" at line "+str(linen)+", num "+str(num))
				searchs = pattern.findall(line)
				print(f"{searchs} was found in line {linen} of {path}")
				if (len(searchs) != 0):
					print("Replacing "+searchs[num]+" with \""+list(strings.values())[stringslinen]+"\" into "+path+" at line "+str(linen)+", num "+str(num))
					lines[linen] = line.replace(searchs[num],"\""+list(strings.values())[stringslinen]+"\"",1)
				else:
					print(f"No string was found in {path}")
			ff.writelines(lines)
			ff.close()
		except:
			print("Error encountered when writing "+dir+"Repacked/"+path)

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