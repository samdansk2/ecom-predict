# program to find leaders in the array , leader is an element which is greater than average of all its adjacent elements.  
# traversed through the array , found average and compares this with each element
arr = [2, 9, 4, 6, 1, 5, 8]
n = len(arr)
leaders = []

sum_right = 0

for i in range(n - 2, -1, -1):
    sum_right += arr[i + 1]
    average = sum_right / (n - i - 1)
    if arr[i] > average:
        leaders.append(arr[i])

print("Leaders in the array:", leaders)
