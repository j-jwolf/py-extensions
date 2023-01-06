import os, sys, inspect, types, subprocess
from shutil import rmtree
from datetime import datetime
try: import pyperclip
except Exception:
	os.system("pip install pyperclip")
	import pyperclip


functionList = list()
stds = [sys.stdin, sys.stdout, sys.stderr]
redirs = [None, None, None]

def toClipboard(s): pyperclip.copy(s)
def logError(error):
	try:
		with open(errorLog, "a") as file: file.write(f"{datetime.now()}\n\t{error}\n")
		return True
	except Exception as e:
		print(f"ERROR WRITING {str(type(e))} TO {errorLog}:\n{e}")
		forceClose(force = True)
	return False
def forceClose(error = None, force = None):
	if force is None: force = False
	if(not force):
		for file in redirs:
			if not file is None: file.close()
		if(error): logError(error)
	sys.exit()
"""
DEPRECATED
"""
def redirectStdin(target):
	try:
		if redirs[0] is None:
			redirs[0] = open(target, "w")
			sys.stdin = redirs[0]
		else:
			redirs[0].close()
			sys.stdin = stds[0]
		return True
	except KeyboardInterrupt: forceClose()
	except Exception as e: print(e)
	return False
def redirectStdout(target):
	try:
		if redirs[1] is None:
			redirs[1] = open(target, "w")
			sys.stdout = redirs[1]
		else:
			redirs[1].close()
			sys.stdout = stds[1]
		return True
	except KeyboardInterrupt: forceClose()
	except Exception as e: print(e)
	return False
def redirectStderr(target):
	try:
		if redirs[2] is None:
			redirs[2] = open(target, "w")
			sys.stderr = redirs[2]
		else:
			redirs[2].close()
			sys.stderr = stds[2]
		return False
	except KeyboardInterrupt: forceClose()
	except Exception as e: print(e)
	return False
"""
========
"""
def exists(fn): return os.path.isfile(fn) or os.path.isdir(fn)
def isfile(fn): return os.path.isfile(fn)
def isdir(fn): return os.path.isdir(fn)
def verifyPath(data):
	buffer = ""
	for letter in data:
		if(letter == "/" or letter == "\\"):
			if(letter == "/" and isWindows()): buffer += "\\"
			elif(letter == "\\" and not isWindows()): buffer += "/"
			else: buffer += letter
		else: buffer += letter
	return buffer
def getModuleLibPath():
	tok = __file__.split(os.path.sep)
	path = ""
	for item in tok:
		if(item != "terminal.py"): path += f"{item}{os.path.sep}"
	return path
def getModulePath(): return __file__
def mergePath(*args):
	buffer = ""
	count = 0
	length = len(args)
	for arg in args:
		buffer += arg
		count += 1
		if(count < length): buffer += os.path.sep
	return buffer
def isWindows(): return sys.platform in {"win32", "msys", "cygwin"}
def pout(command):
	try: os.system(command)
	except Exception as e: print(e)
def ls(path = None):
	if path is None: path = ""
	if(isWindows()): pout(f"dir {path}")
	else: pout(f"ls {path}")
def cd(path):
	try: os.chdir(verifyPath(path))
	except Exception as e: print(e)
def cwd(): print(os.getcwd())
def mkdir(path): os.mkdir(verifyPath(path))
def rmdir(path): rmtree(verifyPath(path))
def less(fn):
	cls()
	if(not os.path.isfile(fn)): return
	with open(fn) as file: print(file.read())
	input("press enter...")
	cls()
def cls():
	if(isWindows()): pout("cls")
	else: pout("clear")
def getcwd(): return os.getcwd()
def mv(file1, file2):
	if(not os.path.isfile(file1)): return
	if(not isWindows()): pout(f"mv {file1} {file2}")
	else: pout(f"move {file1} {file2}")
def cp(file1, file2):
	if(not os.path.isfile(file1)): return
	if(isWindows()): pout(f"copy {file1} {file2}")
	else: pout(f"cp {file1} {file2}")
def rm(fn):
	if(os.path.isdir(fn)): rmdir(fn)
	else:
		if(not os.path.isfile(fn)): return
		if(not isWindows()): pout(f"rm {fn}")
		else: pout(f"del {fn}")
def getFunctionList():
	global functionList
	return functionList
def is_local(object): return isinstance(object, types.FunctionType) and object.__module__ == __name__
def help():
	count = 0
	for function in getFunctionList():
		print(f"{count}: {function}")
		count += 1
def test(): print("test")
def nano(fn, holdIndent = None):
	if holdIndent is None: holdIndent = True
	command = "nano "
	if(holdIndent): command += "-i "
	command += fn
	pout(command)
	return
def lineCount(fn):
	count = 0
	with open(fn) as file: count = len(file.readlines())
	return count
def getLines(fn):
	count = 0
	buffer = ""
	with open(fn) as file: data = file.readlines()
	for line in data:
		count += 1
		buffer += f"{count}: {line}"
	return buffer
def wordCount(fn):
	with open(fn) as file: count = len(file.read().split(" "))
	return count
def characterCount(fn):
	count = 0
	with open(fn) as file: data = file.read()
	for char in data: count += 1
	return count
def echo(*args):
	buffer = " ".join(args)
	os.system(f"echo {buffer}")
	return
def getCInfo(fn):
	base = fn.split(".")[0]
	ext = ".exe"
	if not sys.platform in {"win32", "msys", "cygwin"}: ext = ".bin"
	return (base, ext)
def python(fn, *args):
	if(fn.endswith(".py") and exists(fn)):
		a = ""
		for arg in args: a += " "+str(arg)
		subprocess.Popen(f"python {fn} {a}").wait()
	return
def cpp(fn, *args):
	if(fn.endswith(".cpp") or fn.endswith(".h") and exists(fn)):
		base, ext = getCInfo(fn)
		output = ""
		if not sys.platform in {'win32', 'msys', 'cygwin'}: output = "./"
		subprocess.Popen(f"g++ {fn} -o {base}{ext}").wait()
		arguments = ""
		for arg in args: arguments += " "+str(arg)
		subprocess.Popen(f"{output}{base}{ext} {arguments}").wait()
	return
def c(fn, *args):
	if(fn.endswith(".c") or fn.endswith(".h") and exists(fn)):
		base, ext = getCInfo(fn)
		output = ""
		if(not isWindows()): output = "./"
		subprocess.Popen(f"gcc {fn} -o {base}{ext}").wait()
		arguments = " ".join(args)
		subprocess.Popen(f"{output}{base}{ext} {arguments}").wait()
	return
def java(fn, *args):
	print("under development")
	"""
	this needs a way to get the JVM if it isn't installed
	checkInstalled(java)
	no:
		...
	yes: pass
	"""
	return
	if(fn.endswith(".java") and exists(fn)):
		arguments = " ".join(args)
		subprocess.Popen(f"javac {fn}").wait()
		base = fn.split(".")
		subprocess.Popen(f"java {base}.class").wait()
	return
def toHome(): cd(os.path.expanduser("~"))
def mkcd(dir):
	if(not isdir(dir)): mkdir(dir)
	if(isdir(dir)): cd(dir)

home = mergePath(os.path.expanduser("~"), "Documents", "Python Terminal Module")
if(not os.path.isdir(home)): os.mkdir(home)
errorLog = mergePath(home, "error.log")
functionList = [name for name, value in inspect.getmembers(sys.modules[__name__], predicate=is_local)]
