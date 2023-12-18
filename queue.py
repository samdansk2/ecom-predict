# program to illustrate queuequeue=[]

queue.append(1)
queue.append(2)
queue.append(4)
queue.append(8)

print("queue size",len(queue))

peek=(queue[0])
print("Front element:",peek)

while(len(queue)!=0):
    m= queue.pop(0)
    print("popped element:", m)

print("queue size after popping all elements",len(queue))
      
