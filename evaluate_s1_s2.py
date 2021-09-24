import csv
def evaluate_s1_s2(file,s1,s2):
    
    S1TP=0
    S1TN=0
    S1FP=0
    S2TP=0
    S2TN=0
    S2FP=0
    begin=[]
    end=[]
    event=[]
    
    for x in open(file).readlines():
        begin.append(float(x.split('\t')[0]))
        end.append(float(x.split('\t')[1]))
        event.append(x.split('\n')[0].split('\t')[2])
    #print(begin)
    #print(end)
    #print(event)    
    S1count=0
    S2count=0
    for i in range(1,len(event)):
        ind=[]
   
        if event[i]=='S1':
            #Check if the predicted location of S1 coincides with the annotations
            for value in s1:
                if (value>=begin[i] and value<=end[i]):
                    ind.append(i)
            if ind:
                S1TP=S1TP+1
            else:
                S1TN=S1TN+1
            S1count=S1count+1
        elif event[i]=='S2':
            #Check if the predicted location of S coincides with the annotations
            for value in s2:
                if (value>=begin[i] and value<=end[i]):
                    ind.append(i)
            if ind:
                S2TP=S2TP+1
            else:
                S2TN=S2TN+1
            S2count=S2count+1
        else:
            print(i)
            print("none")
        
        print(len(s1), len(s2))
        S1FP=len(s1)-S1TP
        S2FP=len(s2)-S2TP

    
    return S1TP, S1TN, S1FP, S2TP, S2TN, S2FP
