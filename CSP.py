from collections import OrderedDict 
import random
import heapq

#Defining constraint as a function
def constrain(M,X):
	flag1=0#whether this node is completely filled or not
	flag2=True#whether this node is appropriate according to constraints or not
	if X[M-1][2]>0:
		flag1=True
	ret=0
	#Constraint1,2: Same day same slot , diff prof and diff lecture hall
	for j in range(M):
		for k in range(M):
			if X[j][2]==X[k][2] and X[j][3]==X[k][2]:
				if X[j][1]==X[k][1] or X[j][0]==X[k][0]:
					flag2=False
	#Constraint3: 2 classes of a subject should be scheduled at a diff of atleast 2 days
	for j in range(M/2):
		if abs(X[j][2]-X[j+M/2][2]):
			flag2=False
	#Constraint4: 2 classes of a subject should be scheduled in same lecture Hall
	for j in range(M/2):
		if not (X[j][0]==X[j+M/2][0]):
			flag2=False
	if flag1:
		if flag2:
			return 1#Solution
		else:
			return 0#Not satisfying constraints
	else:
		return 2#unfilled variable

#Print answer
def output(X,M,profs):
	best_ans=X
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
		h=best_ans[j][0]
		d=best_ans[j][1]
		s=best_ans[j][2]
		p=profs[j]
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

#Initial declarations

M=int(input("Enter the number of courses"))
N=int(input("Enter the number of lecture halls"))
P=int(input("Enter the number of professors"))
M*=2#For restricting atleast 2 classes of each course a week.

#Assigning professors for subjects, same professor may take multiple subject, but multiple professor should not take same subject.
profs=[0]*M
for i in range(int(M/2)):
	profs[i]=random.randint(1,P)
	profs[i+int(M/2)]=profs[i]


#Final answer
ans=[0]*M

#Variable declaration

#Specified variables, M variables of size 3 storing hall(j), day(k), slot(l)
var=[0,0,0]

#Specified domains of variables
domain=[]
to_del=[]
for i in range(M):
	domain.append([])
	to_del.append([])

#Alloting all possible values to domain of each subejct
for i in range(M):
	for j in range(N):
		for k in range(5):
			for l in range(8):
				domain[i].append([j,k,l])


#Specified constraints in function at top
#1.difference of 2 day between 2 classes of a subject
#2.same hall for a subject
#3.same day, same slot , not same prof
#4.same day, same slot , not same hall

#Applying most constrained variable, means entry which has least count of available domains

#Store number of possible domains for each variable
dom_cnt=[0]*M
for i in range(M):
	dom_cnt[i]=len(domain[i])

sub_done=[0]*M
done=0
while sub_done.count(0)>0:
	min_dom_val=max(dom_cnt)
	sub_most_constrained=0
	for i in range(M):
		if dom_cnt[i]<=min_dom_val and sub_done[i]==0:
			sub_most_constrained=i
			min_dom_val=dom_cnt[i]
	if dom_cnt[sub_most_constrained]==0:
		sub_done[sub_most_constrained]=1
		continue
	i=random.randint(0,len(domain[sub_most_constrained])-1)
	ans[sub_most_constrained]=domain[sub_most_constrained][i][:]
	hall=ans[sub_most_constrained][0]
	day=ans[sub_most_constrained][1]
	slot=ans[sub_most_constrained][2]
	sub_done[sub_most_constrained]=1
	#Reducing domains of other variables on the basis of value assigned to this variable
	if sub_most_constrained<M/2:
		for j in range(len(domain[sub_most_constrained+M/2])):
			if abs(domain[sub_most_constrained+M/2][j][1]-day)<2 or domain[sub_most_constrained+M/2][j][0]!=hall:
				to_del[sub_most_constrained+M/2].append(j)
	for i in range(M):
		for j in range(len(domain[i])):
			if sub_done[i]==0 and i!=sub_most_constrained and i!=sub_most_constrained+M/2:
				if domain[i][j][2]==hall and domain[i][j][1]==day and domain[i][j][2]==slot:
					to_del[i].append(j)
				if profs[i]==profs[sub_most_constrained] and domain[i][j][1]==day and domain[i][j][2]==slot:
					to_del[i].append(j)
	for i in range(M):
		z=to_del[i]
		to_del[i]=list(set(z))
		to_del[i].sort()

	for i in range(M):
		if sub_done[i]==0:
			while len(to_del[i])>0:
				j=to_del[i][-1]
				domain[i].pop(j)
				to_del[i].pop(-1)
				#print to_del[i][j],len(domain[i])
	for i in range(M):
		to_del[i]=[]

	#recompute domain count for each variable after domain reduction
	for i in range(M):
		dom_cnt[i]=len(domain[i])

output(ans,M,profs)
