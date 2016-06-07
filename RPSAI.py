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
    prediction = choice(choices) #"best move so far" variable
    weight = 0 #weight of the prediction based on algortithm
    for k in range(length-start,length-1): #iterates through shrinking window
        if length==0: #if window non-existant
            return choice(choices)
        ins = "".join(inputs[k:]) #turn inputs from k and on into string
        if ins in history[:-1]: #if input string in history string
            rcount=0
            pcount=0
            scount=0
            prev=-1
            for i in range(history.count(ins)): #iterate through every occurence of input string in history
                prev1=history.find(ins,prev+1)
                if prev1+len(ins) <= len(history)-1: #find next move after input string occurence
                    next1 = history[prev1 + len(ins)]  
                if next1 =="R":
                    rcount+=1
                elif next1=="P":
                    pcount+=1
                else:
                    scount+=1
                prev = prev1
            if max(rcount,pcount,scount)==rcount: #if r most common next move
                move = "R"
            elif max(rcount,pcount,scount)==pcount: #if p most common next move
                move="P"
            elif max(rcount,pcount,scount)==scount: #if s most common next move
                move = "S"
            '''print ins
            print "next is: " + move
            print history.count(ins)
            print "r" + str(rcount)
            print "p" + str(pcount)
            print "s" + str(scount)'''
            cur_weight = history.count(ins)*len(ins)
            if cur_weight > weight:
                prediction = move
                weight = cur_weight
    return beats[prediction]
def gen_rand():
    myfile = open("Random.txt","w+")
    for i in range(10000):
        a = choice(choices)
        myfile.write(a)
        #print a
    myfile.close()
    return

#Runs rock-paper-scissors games until player exits, returns the result.
import time

def RPS():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = raw_input("Name: ")
    to_load = raw_input("Filename: ")
    history=""
    if len(to_load)>0:
        preload = open(to_load, "a+") #File to load data from
        history = preload.read() #Load data
        preload.close()
    #print history
    filename = name+"_"+timestr
    myfile = open(filename,"a+") #File to write to
    myfile.seek(0,2) #Go to end of file
    #Initializations
    cwins=0
    pwins=0
    ties=0
    inputs=[]
    outputs=[]
    counter=0
    print("Choose 'R', 'P' or 'S' to make a move, choose 'E' to exit.")
    #Main game loop
    while True:
        choice1 =raw_input() #Read input
        if choice1!="": #Avoids error with empty input
            choice1=choice1.upper() #Standardize input to caps
        if choice1 == "E": #Exit the main game loop
            break
        if choice1 == "S":
            print "Player: " + str(pwins) + "  Cpu: " +str(cwins)+" Ties: " + str(ties) + " Total played: " + str(counter)
        elif choice1 in list("RPS"): #Valid move
            counter += 1
            move=makeMove(inputs,outputs,history) #Call AI for move
            if beats[move]==choice1: #Player victory
                pwins+=1 #Add points to player
            elif beats[choice1]==move: #Computer victory
                cwins+=1 #Add points to computer
            elif move==choice1:
                ties +=1
            print (choice1 + "  vs.  " + move) #Display round result
            print str(pwins) + " " + str(cwins) #Score update
            if len(inputs)>1:
                history+=inputs[-2]
            inputs.append(choice1)
            outputs.append(move)
            myfile.write(choice1)
        else:
            print "Invalid move"

    myfile.close()    
    return ("Player: " + str(pwins) + "  Cpu: " +str(cwins) +" Ties: " + str(ties) + " Total played: " + str(counter))

            
        
print RPS()
