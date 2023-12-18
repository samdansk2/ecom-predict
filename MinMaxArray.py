# minimum and maximum element in the array
def minmaxi(arr):
    arr.sort()
    element={"min":arr[0],"max":arr[-1]}
    return element
arr=[15,11,9,6,5,2]
element= minmaxi(arr)
print("Minimum is",element["min"])
print("Maximum is",element["max"])
