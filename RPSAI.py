from random import choice
form numpy import prod
import time
choices = list("RPS")
window = 15
print choices
cwins=0
pwins=0
beats = {"R":"P","P":"S","S":"R"}

#####################################################################################
#################################### ALGORITHMS #####################################
#####################################################################################
def w_algo1(w_inputs,w_parameters):
    history = w_inputs[0]
    ins=w_inputs[1]
    input=[history.count(ins),len(ins)]
    return prod([i[0]**i[1] for i in zip(input,w_parameters)])

def w_algo2(w_inputs,w_parameters):
    history = w_inputs[0]
    ins=w_inputs[1]
    return (history.count(ins)**w_parameters[0])/(1.0*(len(ins)**w_parameters[1]))

w_algos = [w_algo1, w_algo2]
#####################################################################################
#####################################################################################
#####################################################################################




#Scans for current pattern in history to predict next player move
def makeMove(inputs,outputs,history,w_algo, w_parameters):
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
            w_inputs = [history,ins]
            cur_weight = w_algos[w_algo-1](w_inputs, w_parameters)
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

def RPS(meta=False, name="", to_load="", algo=1, timestr="", moves_in="", w_parameters=""):
    if not meta:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = raw_input("Name: ")
        to_load = raw_input("Filename: ")
        algo = raw_input("Algo: ")
    history=""
    if len(to_load)>0:
        preload = open(to_load, "a+") #File to load data from
        history = preload.read() #Load data
        preload.close()
    filename = name+"_"+timestr
    metafile = filename+ "_meta"
    myfile = open(filename,"a+") #File to write to
    myfile.seek(0,2) #Go to end of file
    #Initializations
    cwins=0
    pwins=0
    ties=0
    inputs=[]
    outputs=[]
    counter=0
    print("Choose 'R', 'P' or 'S' to make a move, I for summary statistics, choose 'E' to exit.")
    #Main game loop

    while True:
        e_flag=False
        if moves_in=="":
            choices =raw_input() #Read input
        else:
            choices = moves_in
            moves_in =""
        for choice1 in choices:
            if choice1!="": #Avoids error with empty input
                choice1=choice1.upper() #Standardize input to caps
            if choice1 == "E": #Exit the main game loop
                e_flag = True
                break
            if choice1 == "I":
                print "Player: " + str(pwins) + "  Cpu: " +str(cwins)+" Ties: " + str(ties) + " Total played: " + str(counter)
            elif choice1 in list("RPS"): #Valid move
                counter += 1
                move=makeMove(inputs,outputs,history,algo) #Call AI for move
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
        if e_flag and raw_input("Quit? Y/N "):
            break
    myfile.close()
    print ("Player: " + str(pwins) + "  Cpu: " +str(cwins) +" Ties: " + str(ties) + " Total played: " + str(counter))
    return [pwins, cwins, ties, total]


def param_gradient(n=10, w_algo2use =1, config_w_parameters =[[0,5],[0,5]], moves_in="", name="", to_load="", timestr="" ):
    param_names =[]
    best_params=[]
    best_score = 0
    for i in range(len(config_w_parameters)):
        best_params.append(config_w_parameters[i][0])
        param_names.append("param{0}".format(i))
    param_names = ",".join(param_names)
    to_run = ""
    for i in range(len(config_w_parameters)):
        to_run+="\t"*i
        to_run+= "for {0} in range({1},{2}):\n".format(param_names[i],config_w_parameters[i][0], config_w_parameters[i][1])
    to_run+= "\t"*(i+1)
    to_run+="results = RPS(True,{0}, {1}, {2}, {3}, {4}, [{5}])\n".format(name, to_load, w_algo2use, timestr, moves_in, param_names)
    to_run+= "\t"*(i+1)
    to_run+="score = (1.0*results[1])/(1.0*results[3])\n"
    for j in range(n-1):
        to_run+="results = RPS(True,{0}, {1}, {2}, {3}, {4}, [{5}])\n".format(name, to_load, w_algo2use, timestr, moves_in, param_names)
        to_run+= "\t"*(i+1)
        to_run+="score += (1.0*results[1])/(1.0*results[3])\n"
        to_run+= "\t"*(i+1)
    to_run+="score = score/{0}".format(n)
    to_run+="if score > best_score:\n"
    to_run+= "\t"*(i+2)
    to_run+="best_score = score\n"
    to_run+= "\t"*(i+2)
    to_run+="best_params = [{0}]\n".format(param_names)
    return [best_params, best_score]

def meta(n=10, w_algos2use = [1,2] , config_w_parameters = [[[0,5],[0,5]],[[0,5],[0,5]]], moves_in="" ):
    accuracies = {}
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = raw_input("Name: ")
    to_load = raw_input("Filename: ")
    for i in range(len(w_algos2use)):
        w_algo2use = w_algos2use[i]
        accuracies[str(w_algo2use)] = param_gradient(n, w_algo2use,config_w_parameters[i],moves_in,name,to_load, timestr)

    return accuracies






moves_in="RPS"
print meta(moves_in)
