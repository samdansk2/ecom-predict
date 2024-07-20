# Given the names and grades for each student in a class of N students, print the names of  
# students having the second lowest grade.

n=int(input())
ab=[]
grade=[]

for i in range(n):
    name=input()
    mark=float(input())
    ab.append([name,mark])
    grade.append(mark)

grade=sorted(set(grade))
m=grade[1]

name=[]
for value in ab:
    if m == value[1]:
        name.append(value[0])
for cd in name:
    print(cd)

# value is ab's "values name and mark"
