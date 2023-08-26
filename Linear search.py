arr=[2,3,6,7,8]
m=8
flag=0
for i in range(len(arr)):
    if(arr[i]==m):
        flag=1
        print("element found at",i)
        break
if flag==0:
    print("element not found")

        
