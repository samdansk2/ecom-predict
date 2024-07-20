# Python program to illustrate stack data structure

stack=[]

stack.append(1)
stack.append(2)
stack.append(4)

print("stack size",len(stack))

peek=(stack[-1])
print("Top element:",peek)

while(len(stack)!=0):
    m= stack.pop()
    print("popped element:", m)

print("stack size after popping",len(stack))
      
