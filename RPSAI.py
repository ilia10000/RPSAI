from random import choice

choices = list("RPS")
window = 15
print choices
cwins=0
pwins=0
beats = {"R":"P","P":"S","S":"R"}


#Scans for current pattern in history to predict next player move
def makeMove(inputs,outputs,history):
    move = ""
    length = len(inputs)
    start=length
    if length>window:
        start=window
    
    for k in range(length-start,length-1):
        if length==0:
            return choice(choices)
        ins = "".join(inputs[k:])
        if ins in history[:-1]:
            rcount=0
            pcount=0
            scount=0
            prev=-1
            for i in range(history.count(ins)):
                prev1=history.find(ins,prev+1)
                if prev1+len(ins) <= len(history)-1:
                    next1 = history[prev1 + len(ins)]  
                if next1 =="R":
                    rcount+=1
                elif next1=="P":
                    pcount+=1
                else:
                    scount+=1
                prev = prev1
            if max(rcount,pcount,scount)==rcount:
                move = "R"
            elif max(rcount,pcount,scount)==pcount:
                move="P"
            elif max(rcount,pcount,scount)==scount:
                move = "S"
            '''print ins
            print "next is: " + move
            print history.count(ins)
            print "r" + str(rcount)
            print "p" + str(pcount)
            print "s" + str(scount)'''
            return beats[move]
    return choice(choices)

#Runs rock-paper-scissors games until player exits, returns the result.
def RPS():
    myfile = open("F.txt","w+")
    history = myfile.read()
    myfile.seek(0,2)
    cwins=0
    pwins=0
    inputs=[]
    outputs=[]
    print("Choose 'R', 'P' or 'S' to make a move, choose 'E' to exit.")
    #Main game loop
    while True:
        choice1 =raw_input() #Read input
        if choice1!="": #Avoids error with empty input
            choice1=choice1.upper() #Standardize input to caps
        if choice1 == "E": #Exit the main game loop
            break
        elif choice1 in list("RPS"): #Valid move
            move=makeMove(inputs,outputs,history) #Call AI for move
            if beats[move]==choice1: #Player victory
                pwins+=1 #Add points to player
            elif beats[choice1]==move: #Computer victory
                cwins+=1 #Add points to computer
            print (choice1 + "  vs.  " + move) #Display round result
            print str(pwins) + " " + str(cwins) #Score update
            if len(inputs)>1:
                history+=inputs[-2]
            inputs.append(choice1)
            outputs.append(move)
        else:
            print "Invalid move"
    myfile.close()    
    return ("Player: " + str(pwins) + "  Cpu: " +str(cwins))

            
        
print RPS()
