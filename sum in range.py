# Given an array of integers and two integers l and r , find the number of pairs (i, j)  
# such that the value arr[i]+arr[j] lies between l and r, both inclusive.
# i got to know that two loops are used to form pairs in the array , stored their sum in variable
# Compared the sum values according to given inclusive range.
def sam (arr,l,r):
    n=len(arr)
    arr1=[]
    for i in range(n):
        for j in range(i+1,n):
            ab=arr[i]+arr[j]
            print(ab)
            arr1.append(ab)
    count=0
    for i in range(len(arr1)):
        if arr1[i]>=l and arr1[i]<=r:
            count+=1
        else:
            continue
    return count

arr=list(map(int,input().split()))
l=int(input())
r=int(input())
k=sam(arr,l,r)
print(k)
