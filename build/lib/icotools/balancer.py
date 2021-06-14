import csv
import random
import sys


def balancer(csv_file):
    '''
Makes a list of experiments and their items from the words in csv_file.
Balances the experiments so they test a roughly equal number of words.
If you specify whether you think these words will be iconic (y/n), it balances the experiments so they have a roughly equal number of iconic and non-iconic words.
The csv_file should contain the following columns:

form: the forms being tested (e.g. kirakira, fuwafuwa). Your media files should also be named by their form, e.g. kirakira.mp3, or fuwafuwa.mp4
meaning: translations of the form, separated by | (e.g. sparkling|glittering|twinkling)
item: the type of item that form is, available options are 'practice' (a practice item), 'control' (a control item), and 'trial' (a trial/real test item)
iconic: your hypothesis about whether the form is iconic or not. Available values are 'y' or 'n'. This column is optional. If you include it, the function will balance the experiments so that each has a roughly equal number of words thought to be iconic, versus words thought to not be iconic.
'''

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


    # Decide how many experiments to let all these words
    print('You have '+str(len(trials))+'trials, with '+str(len(practice))+'practice items and '+str(len(controls))+' control items.')

    done=False
    no_words=len(trials)
    while not done:
        no_experiments=int(input('How many experiments do you want to have?'))
        division=[no_words // no_experiments + (1 if x < no_words % no_experiments else 0)  for x in range (no_experiments)]
        extra_qs=len(controls)+len(practice)
        items=[x+extra_qs for x in division]
        print('This will result in experiments with the following amount of items')
        print(items)
        choice=input('Is this good? If it is press y, otherwise press n to choose another number of experiments')
        if choice=='y':
            done=True

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

    with open('wordlist_exps.csv','w',newline='',encoding='UTF-8') as outfile:
        writer=csv.writer(outfile)
        writer.writerow(['experiment','item','form','meaning','hypothesis'])
        for i in range(len(experiments)):
            items=experiments[i]
            exp_no=i+1
            for tup in items:
                writer.writerow([exp_no,tup[3],tup[0],tup[1],tup[2]])
    outfile.close()

                
        

