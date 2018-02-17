import pickle

mem=pickle.load( open( "_bytes.pick", "rb" ) )

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
codeXname={}
i=128
for x in vInstr:
	nameXcode[x["name"]]=i
	codeXname[i]=x["name"]
	i+=4

CONDREG=1
MEMREG=0
KEY=0
VISITED=[0]
ASTACK=[]

def readstrz(m,p):
	s=bytearray()
	while True:
		s.append(m[p])
		p+=1
		if m[p]==0:
			break
	return s.decode('utf-8')

ptr=0
while True:
	b=mem[ptr]
	
	if b in codeXname.keys():
		#print(str(ptr)+": "+codeXname[b])
		
		if codeXname[b]=="rest":
			CONDREG = 1
			ptr+=1
			continue
			
		if codeXname[b]=="nop":
			ptr+=1
			continue
			
		if codeXname[b]=="waitkey":
			KEY=int(input())
			ptr+=1
			continue
			#print(KEY)
		
		if codeXname[b]=="condtxt":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			if CONDREG==1:
				print(readstrz(mem,MEMREG))
			else:
				pass
			ptr+=4
			continue
		
		if codeXname[b]=="condact":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			if CONDREG==1:
				print("A:",readstrz(mem,MEMREG), MEMREG)
				ASTACK.append(MEMREG)
			else:
				pass
			ptr+=4
			continue
		
		if codeXname[b]=="onv":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			if mem[MEMREG]==1:
				CONDREG=CONDREG&1
			else:
				CONDREG=CONDREG&0
			
			ptr+=4
			continue
			
		if codeXname[b]=="condset":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			if CONDREG==1:
				mem[MEMREG]=1
			ptr+=4
			continue
			
		if codeXname[b]=="condmes": # условный вывод сообщения при нажатии кнопки
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			
			if CONDREG==1:
				print(readstrz(mem,MEMREG))
			ptr+=4
			continue
			
		if codeXname[b]=="condret":
			if CONDREG==1:
				ptr=VISITED[-2]
				continue
			else:
				ptr+=1
				continue
			
		if codeXname[b]=="condunset":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			if CONDREG==1:
				mem[MEMREG]=0
			ptr+=4
			continue
			
		if codeXname[b]=="offv":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			
			if mem[MEMREG]==1:
				CONDREG=CONDREG&0
			else:
				CONDREG=CONDREG&1
			
			
			#print("\tsetting "+str(CONDREG))
			ptr+=4
			continue
			
		if codeXname[b]=="eq":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			#print(KEY," ",ASTACK)
			if MEMREG==ASTACK[KEY-1]:
				CONDREG=1
			else:
				CONDREG=0
			#print("\teq-setting "+str(CONDREG))
			ptr+=4
			continue
	
		if codeXname[b]=="setname":
			VISITED.append(ptr)
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			print("==",readstrz(mem,MEMREG),"==")
			
			ptr+=4
			ASTACK.clear()
			continue
			
		if codeXname[b]=="condjmp":
			MEMREG = mem[ptr+1]*256*256 + mem[ptr+2]*256 + mem[ptr+3]
			
			if CONDREG==1:
				ptr=MEMREG
				#print("\tgoing "+str(MEMREG))
			else:
				ptr+=4
				#print("\tjust next")
			continue
	else:
		print(str(ptr)+": "+str(b))
	
	ptr+=1
	if ptr>8000:
		break


