arr = [1,3,2,4,5,1,3,2]
sum = 6
ab= set()
for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
        if arr[i] + arr[j] == sum:
            pair = (arr[i], arr[j])
            # Check if the pair is already in the set
            if (pair[0], pair[1]) not in ab and (pair[1], pair[0]) not in ab:
                ab.add(pair)
print(ab)
