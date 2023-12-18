# program to remove all occurences of given value
def sam(arr, val):
    i = 0
    while i < len(arr):
        if arr[i] == val:
            arr.pop(i)
        else:
            i += 1

    return len(arr)

arr = [3,2,1,3,4,3,5]
val = 3
w = sam(arr, val)
print(w)
