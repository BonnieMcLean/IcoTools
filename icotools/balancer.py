import csv
import random
import sys
import math


def balancer(csv_file,no_expwords):

    # read in the file and make a list of trials, practice_qs, and controls
    
    trials=[]
    practice=[]
    controls=[]
    iconic_count=0
    arb_count=0
    with open(csv_file,encoding='UTF-8') as infile:
        reader=csv.DictReader(infile)
        for row in reader:
            try:
                form=row['form']
                meaning=row['meaning']
                item=row['item']
            except KeyError:
                print('Your csv file is not formatted correctly. See help(balanced_exps) for information on how to format it correctly.')
            try:
                iconic=row['iconic']
                # keep track of how many trials are iconic versus arb
                if iconic=='y':
                    hypothesis='iconic'
                    if item=='trial':
                        iconic_count+=1
                else:
                    hypothesis='not iconic'
                    if item=='trial':
                        arb_count+=1

            except KeyError:
                hypothesis='none'
                
            # store the trials, practice and control items
            if item=='trial':
                trials.append((form,meaning,hypothesis,item))
            elif item=='practice':
                practice.append((form,meaning,hypothesis,item))
            else:
                controls.append((form,meaning,hypothesis,item))
    infile.close()


    # Decide how many experiments to test all these words

    no_words=len(trials)
    no_experiments=math.ceil((no_words/no_expwords))
    division=[no_words // no_experiments + (1 if x < no_words % no_experiments else 0)  for x in range (no_experiments)]
    # shuffle the trials
    random.shuffle(trials)

    # balance the iconic and non-iconic words if you have that information specified

    # balance the iconic words evenly across the experiments
    iconic_groups=[iconic_count // no_experiments + (1 if x < iconic_count % no_experiments else 0)  for x in range (no_experiments)]
    # balance the prosaic words evenly across the experiments
    prosaic_groups=[arb_count // no_experiments + (1 if x < arb_count % no_experiments else 0)  for x in range (no_experiments)]

    # make a structure to store the experiments
    experiments=[]
    for i in range(no_experiments):
        experiments.append([])

    # if you have a mix of iconic and prosaic words, balance them across the experiments
    if sum(iconic_groups)>0 and sum(prosaic_groups)>0:
        exp_index=0
        for i in range(len(iconic_groups)):
            no_iconic=iconic_groups[i]
            no_prosaic=prosaic_groups[i]
            
            # first add iconic words
            while no_iconic!=0:
                trial=trials.pop(0)
                if trial[2]=='iconic':
                    experiments[exp_index].append(trial)
                    no_iconic=no_iconic-1
                else:
                    trials.append(trial)
            # then add the prosaic words
            while no_prosaic!=0:
                trial=trials.pop(0)
                if trial[2]=='not iconic':
                    experiments[exp_index].append(trial)
                    no_prosaic=no_prosaic-1
                else:
                    trials.append(trial)
                    
            # move to the next experiment
            exp_index+=1
    else:
        # if the words are all the same you don't need to balance them across trials, just follow the divisions
        exp_index=0
        for num in division:
            for i in range(num):
                trial=trials.pop(0)
                experiments[exp_index].append(trial)
            exp_index+=1
                
    # now add the practice and control items to all the experiments
    for exp in experiments:
        index=experiments.index(exp)
        experiments[index]=practice+exp+controls

    # now write the experiments file
    filename=csv_file+'_experimentlist'
    with open(filename,'w',newline='',encoding='UTF-8') as outfile:
        writer=csv.writer(outfile)
        writer.writerow(['experiment','item','form','meaning','hypothesis'])
        for i in range(len(experiments)):
            items=experiments[i]
            exp_no=i+1
            for tup in items:
                writer.writerow([exp_no,tup[3],tup[0],tup[1],tup[2]])
    outfile.close()

                
        

