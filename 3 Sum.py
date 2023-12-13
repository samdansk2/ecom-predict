arr=[1,3,2,5,6,4,1,1]
target_sum= 6
sum=0

n=len(arr)
sub=[]
pairs=[]
for i in range(n-1,-1,-1):
    sum+=arr[i]
    sub.append(arr[i])

    if sum==target_sum and len(sub)==3:
        print(sub)
        pairs.append(sub.copy())

    while sum>target_sum:
        m=sub.pop(0)
        sum=sum-m

if not pairs:
    print("no elements found")
    

