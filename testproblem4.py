arr = [3,2,7,6,1,2,5,3,1]
target_sum = 13
n = len(arr)
sum = 0
subarray = []

for i in range(n - 1, -1, -1):
    sum += arr[i]
    subarray.append(arr[i])
    
    while sum > target_sum and subarray:
        sum -= subarray.pop(0)
    
    if sum == target_sum and len(subarray) == 4:
        print(subarray)
else:
    print("no elements found")
