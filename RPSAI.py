from random import choice
from numpy import prod, arange
import time
import os
choices = list("RPS")
window = 25
print choices
cwins=0
pwins=0
beats = {"R":"P","P":"S","S":"R"}

#####################################################################################
#################################### ALGORITHMS #####################################
#####################################################################################
def w_algo1(w_inputs,w_parameters=[2.1,9.9]):
    history = w_inputs[0]
    ins=w_inputs[1]
    input=[history.count(ins),len(ins)]
    return prod([i[0]**i[1] for i in zip(input,w_parameters)])

def w_algo2(w_inputs,w_parameters=[0.2,9.2]):
    history = w_inputs[0]
    ins=w_inputs[1]
    return (history.count(ins)*w_parameters[0])/(1+1.0*(len(ins)*w_parameters[1]))

def w_algo3(w_inputs,w_parameters=[1,1]):
    history = w_inputs[0]
    ins=w_inputs[1]
    return (history.count(ins)*w_parameters[0])+(len(ins)*w_parameters[1])
def w_algo4(w_inputs,w_parameters=[1,9,0.1]):
    history = w_inputs[0]
    ins=w_inputs[1]
    interaction = history.count(ins)*len(ins)
    return (history.count(ins)*w_parameters[0])+(len(ins)*w_parameters[1]) + (interaction*w_parameters[2])

w_algos = [w_algo1, w_algo2, w_algo3, w_algo4]
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
            if len(w_parameters)>0:
                cur_weight = w_algos[w_algo-1](w_inputs, w_parameters)
            else:
                cur_weight = w_algos[w_algo-1](w_inputs)
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

def RPS(meta=False,debug=False, name="", to_load="", w_algo=1, timestr="", moves_in="", w_parameters=[], threshold = 0.5, direction=0):
    if not meta:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = raw_input("First Name: ") + "_" + raw_input("Last Name: ")
        to_load = raw_input("Filename to load: ")
        w_algo = input("Algo: ")
    history=""
    if len(to_load)>0:
        preload = open(to_load, "a+") #File to load data from
        history = preload.read() #Load data
        preload.close()
    filename = name+"/"+name+"_"+timestr
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    metafile = filename+ "_meta"
    if not meta:
        myfile = open(filename,"a+") #File to write to
        myfile.seek(0,2) #Go to end of file
    #Initializations
    cwins=0
    pwins=0
    ties=0
    inputs=[]
    outputs=[]
    counter=0
    if not meta:
        print("Choose 'R', 'P' or 'S' to make a move, I for summary statistics, choose 'E' to exit.")
    #Main game loop

    while True:
        e_flag=False
        start = time.time()
        if moves_in=="":
            choices =raw_input() #Read input
        else:
            choices = moves_in
            moves_in =""
        elapsed = time.time()-start
        if len(choices):
            average = float(elapsed)/len(choices)
        else:
            average=elapsed
        for choice1 in choices:
            if choice1!="": #Avoids error with empty input
                choice1=choice1.upper() #Standardize input to caps
            if choice1 == "E": #Exit the main game loop
                e_flag = True
                break
            if choice1 == "I":
                print "Player: " + str(pwins) + "  Cpu: " +str(cwins)+" Ties: " + str(ties) + " Total played: " + str(counter)
            elif choice1 in list("RPS"): #Valid move
                if (direction and average > threshold) or (average <= threshold):
                    counter += 1
                    move=makeMove(inputs,outputs,history,w_algo, w_parameters) #Call AI for move
                    if beats[move]==choice1: #Player victory
                        pwins+=1 #Add points to player
                    elif beats[choice1]==move: #Computer victory
                        cwins+=1 #Add points to computer
                    elif move==choice1:
                        ties +=1
                    if not meta:
                        print "Time: " + str(average)
                        print (choice1 + "  vs.  " + move) #Display round result
                        print str(pwins) + " " + str(cwins) #Score update
                    if len(inputs)>1:
                        history+=inputs[-2]
                    inputs.append(choice1)
                    outputs.append(move)
                    if not meta:
                        myfile.write(choice1)
                elif direction:
                    print "Please play slower than {0} secs per move".format(threshold)
                else:
                    print "Please play faster than {0} secs per move".format(threshold)
                
            else:
                print "Invalid move"
        if e_flag and (meta or raw_input("Quit? Y/N ").lower()=="y"):
            break
    if not meta:
        myfile.close()
    if not meta or debug:
        print (" Player: " + str(pwins) + "  Cpu: " +str(cwins) +" Ties: " + str(ties) + " Total played: " + str(counter))
        print ("w_Algo: " + str(w_algo)+ " Params: " + ", ".join(map(str,w_parameters)))
    return [pwins, cwins, ties, counter]

def score_game(inputs):
    pwins = inputs[0]
    cwins = inputs[1]
    ties = inputs[2]
    counter = inputs[3]
    #return cwins/(1.0*counter)
    return cwins/(1.0*pwins +1.0*cwins)
#####################################################################################
#################################### REGRESSORS #####################################
#####################################################################################

def param_brute_force(n=10, w_algo2use =1, config_w_parameters =[[0,5,1],[0,5,1]], moves_in="", name="", to_load="", timestr="" ):
    param_names =[]
    best_params=[]
    best_score = 0
    for i in range(len(config_w_parameters)):
        best_params.append(config_w_parameters[i][0])
        param_names.append("param{0}".format(i))

    to_run = ""
    for i in range(len(config_w_parameters)):
        to_run+="\t"*i
        to_run+= "for {0} in arange({1},{2},{3}):\n".format(param_names[i],config_w_parameters[i][0], config_w_parameters[i][1],config_w_parameters[i][2])
    to_run+= "\t"*(i+1)
    to_run+="results = RPS(True,'{0}', '{1}', {2}, '{3}', '{4}', [{5}])\n".format(name, to_load, w_algo2use, timestr, moves_in, ",".join(param_names))
    to_run+= "\t"*(i+1)
    to_run+="score = score_game(results)\n"
    to_run+= "\t"*(i+1)
    for j in range(n-1):
        to_run+="results = RPS(True,'{0}', '{1}', {2}, '{3}', '{4}', [{5}])\n".format(name, to_load, w_algo2use, timestr, moves_in, ",".join(param_names))
        to_run+= "\t"*(i+1)
        to_run+="score += score_game(results)\n"
        to_run+= "\t"*(i+1)
    to_run+="score = score/{0}\n".format(n)
    to_run+= "\t"*(i+1)
    to_run+="if score > best_score:\n"
    to_run+= "\t"*(i+2)
    to_run+="best_score = score\n"
    to_run+= "\t"*(i+2)
    to_run+="best_params = [{0}]\n".format(",".join(param_names))
    if debug:
        print to_run
    exec(to_run)
    print ("w_Algo: " + str(w_algo2use)+ " Params: " + ", ".join(map(str,best_params)) + " Score: " + str(best_score))
    #print (best_params, best_score)
    return [best_params, best_score]

def param_regression(debug=False,n=10, w_algo2use =1, config_w_parameters =[[0,5,1],[0,5,1]], moves_in="", name="", to_load="", timestr="", direction=0, fast_mode = False ):
    param_names =[]
    best_params=[]


    for i in range(len(config_w_parameters)):
        best_params.append(config_w_parameters[i][direction]-direction*config_w_parameters[i][2])
        param_names.append("param{0}".format(i))
    best_score = 0
    for k in range(n):
        results = RPS(True,debug,name, to_load, w_algo2use, timestr, moves_in, best_params)
        best_score += score_game(results)
    best_score = best_score/n
    print best_score, best_params
    for i in range(len(config_w_parameters)):
        params = [p for p in best_params]

        for j in arange(config_w_parameters[i][0]+1*config_w_parameters[i][2]-direction*config_w_parameters[i][2],config_w_parameters[i][1]-direction*config_w_parameters[i][2],config_w_parameters[i][2])[::(direction*(-2))+1]:
            params[i]=j
            print best_params, params

            cur_score = 0
            for k in range(n):
                results = RPS(True,debug,name, to_load, w_algo2use, timestr, moves_in, params)
                cur_score += score_game(results)
            cur_score = cur_score/n
            if cur_score < best_score:
                print cur_score, best_score
                if fast_mode:
                    print "Local Minima reached"
                    break
            elif cur_score >= best_score:
                best_params = [p for p in params]
                best_score = cur_score
            print best_score, best_params
    print ("w_Algo: " + str(w_algo2use)+ " Params: " + ", ".join(map(str,best_params)) + " Score: " + str(best_score))
    return [best_params, best_score]

def meta(debug=False, n=10, w_algos2use = [1,2] , config_w_parameters = [[[0,10,1],[0,10,1]],[[0,3,1],[0,3,1]]], moves_in="", name="I", to_load="" ):
    accuracies = {}
    timestr = time.strftime("%Y%m%d-%H%M%S")
    #name = raw_input("Name: ")
    #to_load = raw_input("Filename: ")
    for i in range(len(w_algos2use)):
        w_algo2use = w_algos2use[i]
        print "Running w_algo: " + str(w_algo2use)
        accuracies[str(w_algo2use)]={}
        best = param_regression(debug, n, w_algo2use,config_w_parameters[i],moves_in,name,to_load, timestr, direction = 1, fast_mode = False)
        accuracies[str(w_algo2use)]["params"] = best[0]
        accuracies[str(w_algo2use)]["score"] = best[1]

    return accuracies

#####################################################################################
#####################################################################################
#####################################################################################


def run_meta(debug=False):
    moves=open("sample_moves.txt", "r").read()
    for k in [5,15,25,35]:
        window = k
        print "Window: " + str(window)

        print meta(n=4, w_algos2use = [3], config_w_parameters = [[[-10,10,2],[-10,10,2]]], moves_in=moves)

if __name__ == "__main__":
    print RPS()
