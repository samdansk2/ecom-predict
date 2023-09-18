year1=int(input("enter year:"))
year2=int(input("enter year:"))
count=0
for i in range(year1,year2):
    if (i % 400 == 0) and (i % 100 == 0):
        count+=1
    elif (i % 4 ==0) and (i % 100 != 0):
        count+=1
    else:
        count=max(count,0)
print("Number of leap years is ",count)
    
    
                
