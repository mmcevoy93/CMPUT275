myinput = input()

numberofuppers = 0
for i in range(len(myinput)):
    if myinput[i].isupper():
        numberofuppers+=1
print(numberofuppers)
