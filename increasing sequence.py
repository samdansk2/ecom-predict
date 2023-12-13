arr = [1,3,2,4,6,7,5,4]

n=len(arr)
arr1=[]
arr2=[arr[0]]

for i in range(1,n):
    if arr[i] > arr2[-1]:
        arr2.append(arr[i])
    else:
        if len(arr2)>len(arr1):
            arr1=arr2.copy()
        arr2= [arr[i]]
print(arr1)
    
    
