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
