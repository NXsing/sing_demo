import pickle

vCom=pickle.load( open( "SOURCE/_quest.pick", "rb" ) )
vInstr=[]

def add(name, sz1=None, sz2=None):
	global vInstr
	vInstr.append({"name":name, "sz1": sz1, "sz2": sz2 })

add("rest",1)
add("nop",1)
add("setroom",1)
add("condret",1)
add("setsequ",1)
add("waitkey",1)

add("onv" , 1,3)
add("offv", 1,3)
add("condtxt", 1,3)
add("condact", 1,3)
add("condjmp", 1,3)
add("condset", 1,3)
add("condunset", 1,3)
add("setname", 1,3)
add("eq", 1,3)
add("condmes", 1,3)

nameXcode={}
i=128
for x in vInstr:
	nameXcode[x["name"]]=i
	i+=4

print(vInstr)
print(nameXcode)

ptr=0
mem=bytearray(8000)

ptrXname={}
nameXptr={}

def comm(val):
	global ptr,mem
	mem[ptr] = val
	ptr+=1

def comm3(val):
	for b in val.to_bytes(3, byteorder='big', signed=False):
		comm(b)


for c in vCom:
	
	name=c[0]
	arg1=c[1]
	arg2=c[2]
	
	
	#print(name, arg1, arg2)
	
	if name=="rest" or name=="nop" or name=="condret" or name=="waitkey" or name=="setroom" or name=="setsequ":
		comm(0)
	
	if name=="condjmp" or name=="condset" or name=="condunset" or name=="eq" or name=="condact" or name=="onv" or name=="offv" or name=="condtxt" or name=="setname" or name=="condmes":
		comm(0)
		comm3(0)
	
	if name=="byte0" or name=="byte1":
		nameXptr[arg1]=ptr
		ptrXname[ptr]=arg1
		comm(0)
	
	if name=="decl":
		nameXptr[arg1]=ptr
		ptrXname[ptr]=arg1
		for b in arg2.encode('utf-8'):
			comm(0)
		comm(0)
	
	if name=="label":
		nameXptr[arg1]=ptr
		ptrXname[ptr]=arg1
	

ptr=0

for c in vCom:
	
	name=c[0]
	arg1=c[1]
	arg2=c[2]
	
	
	print(name, arg1, arg2)
	if name=="rest" or name=="nop" or name=="condret" or name=="waitkey" or name=="setroom" or name=="setsequ":
		comm(nameXcode[name])

	if name=="condjmp" or name=="condset" or name=="condunset" or name=="eq" or name=="condact" or name=="onv" or name=="offv" or name=="condtxt" or name=="setname" or name=="condmes":
		comm(nameXcode[name])
		try:
			comm3(nameXptr[arg1])
		except:
			raise("ERR: no such name in the database(no room or no var with this name: ")
	
	if name=="byte0":
		comm(0)
	
	if name=="byte1":
		comm(1)
	
	if name=="decl":
		for b in arg2.encode('utf-8'):
			comm(b)
		comm(0)

#print(mem)

import base64

#print(("""var mem=toByteArray("{}")""".format(base64.b64encode(mem))))

res=""
for b in base64.b64encode(mem):
	res+=chr(b)


open("HTML/_bytes.js","w").write("""var mem=toByteArray("{}")""".format(res))

pickle.dump(mem, open( "SOURCE/_bytes.pick", "wb" ) )
