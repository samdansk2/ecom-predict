# program to return all the array elements with frequency 1
# used the count function and stored it in one variable 
arr=[1,2,3,2,4,5,4]
for i in range(len(arr)):
    temp=arr.count(arr[i])
    if(temp==1):
        print(arr[i])
        
