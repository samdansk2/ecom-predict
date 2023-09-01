arr=[9,5,6,3,2,1,4,8]
arr.sort()
for i in range(1,len(arr)):
    if (arr[i] == arr[i - 1]+ 1):
        continue
    else:
        missing_number = arr[i]-1
print(missing_number)
