arr=[2,3,4,3,2]
arr1=[]
for i in range(len(arr)):
    if arr[i] not in arr1:
        temp=arr.count(arr[i])
        print(arr[i],"-",temp)
        arr1.append(arr[i])
