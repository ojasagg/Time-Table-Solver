from collections import OrderedDict 
import random
import heapq
import time
best_ans=[]
best_ans_val=0
#Print answer

def output():
	subject=[0]*M
	arr=[]
	row=[0,0,0,0,0,0,0,0]
	for j in range(5):
		arr.append(row[:])
	for j in range(0,5):
		for k in range(0,8):
			arr[j][k]=[]
	for j in range(int(M/2)):
		subject[j]=j+1
		subject[j+int(M/2)]=j+1
	for j in range(M):
		h=best_ans[0][j]
		p=best_ans[1][j]
		d=best_ans[2][j]
		s=best_ans[3][j]
		newlist=[]
		newlist.append(subject[j])
		newlist.append(p)
		newlist.append(h)
		arr[d-1][s-1].append(newlist)
	print( "\nDay     \t1st     \t2nd     \t3rd     \t4th     \t5th     \t6th     \t7th     \t8th\n")
	dcount=1
	daydict= {}
	daydict[1]="Mon"
	daydict[2]="Tue"
	daydict[3]="Wed"
	daydict[4]="Thu"
	daydict[5]="Fri"
	len_arr=len(arr)
	for row in range(len_arr):
		maxc=0
		len_row=len(arr[row])
		for period in range(len_row):
			l=len(arr[row][period])
			maxc=max(l,maxc)
		flag=0
		m=1
		while m<maxc+1:
			line="     "
			for period in range(len_row):
				flag1=len(arr[row][period])>=m
				if(flag1):
					
					#line+=str(period[m-1])+"     \t"
					line+="S"+str(arr[row][period][m-1][0])+"_P"+str(arr[row][period][m-1][1])
					line+="_H"+str(arr[row][period][m-1][2])+"     \t"
				else:
					line+="             \t"
			flag2=(flag==0)
			if flag2:
				print(str(daydict[dcount])+"     "+line)
			else:
				print("        "+line)
			flag=1
			m+=1
		print("\n\n")
		dcount+=1
	print "Time taken= "+str(time.time()-strt_tme)+"sec"

#Stopping criteria
def stop_criteria(population,M):
	ret=0
	for i in population:
		c=0
		for j in range(M):
			for k in range(M):
				if population[i][2][j]==population[i][2][k] and population[i][3][j]==population[i][2][k]:
					if population[i][1][j]==population[i][1][k] or population[i][0][j]==population[i][0][k]:
						c=1
	if c==0:		
		output()
		exit()
	return 0

#Fitness function
def fitness(pop,entry,M):
	score=0
	for i in pop:
		for j in range(int(M/2)):
			#constraint1
			if pop[i][2][j]!=pop[i][2][j+int(M/2)]:
				score+=100
			#constraint2
			if pop[i][2][j]-pop[i][2][j+int(M/2)]>=2:
				score+=100
			#constraint3
			if pop[i][0][j]==pop[i][0][j+int(M/2)]:
				score+=100
	c4=0
	c5=0
	for i in population:
		for j in range(M):
			for k in range(M):
				if population[i][2][j]==population[i][2][k] and population[i][3][j]==population[i][2][k]:
					#constraint4
					if population[i][1][j]==population[i][1][k]:
						c4=1
					#constraint5
					if population[i][0][j]==population[i][0][k]:
						c5=1
	score-=c4*100
	score-=c5*100
	return score


#Initial declarations

M=int(input("Enter the number of courses"))
N=int(input("Enter the number of lecture halls"))
P=int(input("Enter the number of professors"))
strt_tme=time.time()
M*=2#For restricting atleast 2 classes of each course a week.
D=5
S=8
top_k=15#out of total population, top 15 parents would be selected.
chromosome=[[],[],[],[]]

#Assigning professors for subjects, same professor may take multiple subject, but multiple professor should not take same subject.
profs=[0]*M
for i in range(int(M/2)):
	profs[i]=random.randint(1,P)
	profs[i+int(M/2)]=profs[i]


#Randomly initialize population
population={}
for i in range(50):
	chromo=[]
	for l in chromosome:
		chromo.append(l[:])
	for m in range(M):
		chromo[0].append(random.randint(1,N))
	for m in range(M):
		chromo[1].append(profs[m])
	for m in range(M):
		chromo[2].append(random.randint(1,5))
	for m in range(M):
		chromo[3].append(random.randint(1,8))
	population[str(chromo)]=chromo

#Assigning first random chromosome as best answer, it can be updated futher
	best_ans=chromo

#Evaluating population
value=[]#priority queue to store population in increasing order of fitness value
for i in population:
	val=fitness(population,i,M)
	value.append([val,i])
	if value[0][0]>best_ans_val:
		best_ans=population[i]
heapq._heapify_max(value) 

iterations=0
while(not stop_criteria(population,M) and iterations<1000):
	print("Iteration "+str(iterations+1)+" going on")

	#Selecting parents
	new_population={}
	for i in range(top_k):
		new_population[value[i][1]]=population[value[i][1]]
	population=new_population.copy()
	new_population.clear()

	#Crossover to produce children
	new_population=population.copy()
	for i in population:
		for j in population:
			p1=[]
			p2=[]
			c1=[]
			c2=[]
			for l in population[i]:
				p1.append(l[:])
			for l in population[j]:
				p2.append(l[:])
			one_point=random.randint(0,M)
			for k in range(4):
				c1.append(p1[k][:one_point]+p2[k][one_point:])
				c2.append(p2[k][:one_point]+p1[k][one_point:])
			new_population[str(c1)]=c1
			new_population[str(c2)]=c2
	population.clear()
	population=new_population.copy()
	new_population.clear()

	#Evaluating population
	del value[:]
	for i in population:
		val=fitness(population,i,M)
		value.append([val,i])
		if value[0][0]>best_ans_val:
			best_ans=population[i]
	heapq._heapify_max(value) 
	iterations+=1
print "This might not be the best answer, but the most preferable one."
output()

#contraints
#different days for 2 classes of a subject
#difference of 2 day between 2 classes of a subject
#same hall for a subject
#same day, same slot , not same prof
#same day, same slot , not same hall
