import os
import codecs
import csv
import sys
import math
import random


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

            try:
                foils=row['foils']
            except KeyError:
                foils=''
            try:
                nofoils=row['no_foils']
            except KeyError:
                nofoils=''
                
            # store the trials, practice and control items
            if item=='trial':
                trials.append((form,meaning,hypothesis,item,foils,nofoils))
            elif item=='practice':
                practice.append((form,meaning,hypothesis,item,foils,nofoils))
            else:
                controls.append((form,meaning,hypothesis,item,foils,nofoils))
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

##    # now write the experiments file
##    filename=csv_file.strip('.csv')+'_experimentlist.csv'
##    with open(filename,'w',newline='',encoding='UTF-8') as outfile:
##        writer=csv.writer(outfile)
##        writer.writerow(['experiment','item','form','meaning','hypothesis'])
##        for i in range(len(experiments)):
##            items=experiments[i]
##            exp_no=i+1
##            for tup in items:
##                writer.writerow([exp_no,tup[3],tup[0],tup[1],tup[2]])
##    outfile.close()
        return(experiments)


def guesser(wordlist,control_file):
    """Makes gue"""

    # read in the information from the control file
    control={}
    with open(control_file,'r',encoding='UTF-8') as infile:
        reader=csv.reader(infile)
        for row in reader:
            key=row[0]
            value=row[1]
            control[key]=value
    try:
        no_practiceq=int(control['n_practiceq'])
        media_source=control['media_source']
        media_type=control['media_type']
        muted_vids=control['muted_vids']
        instructions_html=control['instructions_html']
        exitques_html=control['exitques_html']
        headphone_check=control['headphone_check']
        words_per_exp=int(control['words_per_exp'])
    except KeyError:
        print('Your control file is not formatted correctly. See help(guesser) for information on how to format it.')
    if instructions_html=='default':
        instructions_html='guesses_instructions_'+media_type+'.html'
    if exitques_html=='default':
        exitques_html='guesses_exitques.html'

    if media_type!='mp3' and media_type!='mp4':
        print('Please enter a valid media type. Valid media types are mp3 or mp4.')
        return

    # call balancer to make the experiments
    experiments_raw=balancer(wordlist,words_per_exp)

    # make a list of all the words here in the case that you are just
    # using simple foils
    simple_foils=[]

    # make a neat dictionary to store experiments
    experiments={}

    n=1
    for exp in experiments_raw:
        experiments[str(n)]=[]
        for item in exp:
            form=item[0]
            meanings=item[1].upper().split('|')
            hypothesis=item[2]
            item_type=item[3]
            foils=item[4].split('|')
            nofoils=item[5].split('|')
            simple_foils.append(form)
            experiments[str(n)].append([form,foils,meanings,nofoils,hypothesis,item_type])
        n+=1
    
    # in the case where you have simple foils, figure out what the
    # foil list for each word is

    for exp in experiments:
        itemlist=experiments[exp]
        for i in range(len(itemlist)):
            form=itemlist[i][0]
            foils=itemlist[i][1]
            no_foils=itemlist[i][3]
            if foils[0]=='':
                true_foils=list(simple_foils)
                true_foils.remove(form)
                if no_foils[0]!='':
                    for item in no_foils:
                        true_foils.remove(item)
                experiments[exp][i][1]=true_foils
            

    # make experiments list
    filename=wordlist.strip('.csv')+'_experiments.csv'
    with open(filename,'w',newline='') as outfile:
        writer=csv.writer(outfile)
        writer.writerow(('experiment','item_type','form','meaning','foils','hypothesis'))
        for exp in experiments:
            items=experiments[exp]
            for item in items:
                writer.writerow((exp,item[5],item[0],'|'.join(item[2]),'|'.join(item[1]),item[4]))
    outfile.close()
                                
    # get together the code for the guessing experiments
    
    intro_code=[]
    odd_trial=[]
    even_trial=[]
    outro_code=[]
    here = os.path.dirname(os.path.abspath(__file__))
    if media_type=='mp4':
        template=codecs.open(os.path.join(here,'templates','guesses_mp4.html'),'r','utf-8')
    else:
        template=codecs.open(os.path.join(here,'templates','guesses_mp3.html'),'r','utf-8')
    
    section=1
    for line in template:
        if section==1:
            # intro code
            intro_code.append(line)
            if '<!---TRIAL START!---->' in line:
                section+=1
        elif section==2:
            # real test items
            odd_trial.append(line)
            if '<!---EVEN TRIAL!---->' in line:
                section+=1
        elif section==3:
            even_trial.append(line)
            if '<!---TRIAL END!---->' in line:
                section+=1   
        else:
            # outro code
            myline=line
            if "$('#participate').click(showAudioTest);" in line:
                if headphone_check=='n':
                    myline=line.replace('showAudioTest','easystart')
            outro_code.append(myline)

    # add instructions to the intro code

    instructions=codecs.open(os.path.join(here,'templates',instructions_html),'r','utf8')
    instructions_l=[]
    for line in instructions:
        instructions_l.append(line)

    # split intro code into two by line INSTRUCTIONS
    for i in range(len(intro_code)):
        if 'INSTRUCTIONS' in intro_code[i]:
            index=i
    intro_code_1=intro_code[:index]
    intro_code_2=intro_code[index+1:]
    intro_code=intro_code_1+instructions_l+intro_code_2
    

    # add exit quest to the outro code
    exitques=codecs.open(os.path.join(here,'templates',exitques_html),'r','utf-8')
    exit_l=[]
    for line in exitques:
        exit_l.append(line)

    # split outro code into two by line EXIT QUESTIONS
    for i in range(len(outro_code)):
        if 'OUTRO_QUESTIONS' in outro_code[i]:
            index=i

    outro_code_1=outro_code[:index]
    outro_code_2=outro_code[index+1:]
    outro_code=outro_code_1+exit_l+outro_code_2

    
    # make the code for each experiment, and store that in all_experiments
    all_experiments=[]
    for exp in experiments:
        code=[]

        # first the intro code
        for line in intro_code:
            if 'experimentX.php' in line:
                code.append(line.replace('X',exp))
            else:
                code.append(line)

        # then the trial code
        trials=experiments[exp]
        n=1

        # keep track of all the foils, and all the trans in order, as you need to
        # put these in the outro code at the end

        allfoils=[]
        alltrans=[]
        
        for trial in trials:
            foils=trial[1]
            trans=trial[2]
            for i in range(len(foils)):
                foils[i]=media_source+'/'+foils[i]+'.'+media_type

            allfoils.append(foils)
            alltrans.append(trans)

            # I have different odd and even trials because in the even trials the answer is A,
            # in the odd trials the answer is B.
          
            if n%2!=0:
                trial_code=odd_trial
            else:
                trial_code=even_trial
            for line in trial_code:
                if '<div id="trial1" class="trialDiv">' in line:
                    myline=line.replace('trial1','trial'+str(n))
                elif "id='trans1'" in line:
                    myline=line.replace('trans1','trans'+str(n))
                elif 'name="chosentrans1"' in line:
                    myline=line.replace('chosentrans1','chosentrans'+str(n))
                elif "id='realplayer-1'" in line:
                    myline=line.replace('realplayer-1','realplayer-'+str(n))
                    if media_type=='mp4' and muted_vids=='n':
                        myline=myline.replace('muted','')
                elif "id='foilplayer-1'" in line:
                    myline=line.replace('foilplayer-1','foilplayer-'+str(n))
                    if media_type=='mp4' and muted_vids=='n':
                        myline=myline.replace('muted','')
                elif 'id="chosenfoil1"' in line:
                    myline=line.replace('chosenfoil1','chosenfoil'+str(n))                    
                elif "ANSWER_MEDIA" in line:
                    word=trial[0]
                    myline=line.replace('ANSWER_MEDIA',media_source+'/'+word+'.'+media_type+'"&someRandomSeed=" + Math.random().toString(36)')
                elif 'options1' in line:
                    myline=line.replace('options1','options'+str(n))
                elif 'q1' in line:
                    myline=line.replace('q1','q'+str(n))
                elif 'ques1' in line:
                    myline=line.replace('ques1','ques'+str(n))
                elif 'reactionTime1' in line:
                    myline=line.replace('reactionTime1','reactionTime'+str(n))
                    myline=myline.replace('rt1','rt'+str(n))
                else:
                    myline=line
                code.append(myline)
            n+=1

        # then finally the outro code
        for line in outro_code:
            if 'allfoils=[[],[]]' in line:
                begin='[['
                for i in range(len(allfoils)):
                    items=allfoils[i]
                    for z in range(len(items)):
                        if z==len(items)-1:
                            if i==len(allfoils)-1:
                                begin+='"'+items[z]+'"]]'
                            else:
                                begin+='"'+items[z]+'"],['
                        else:
                            begin+='"'+items[z]+'",'
                    
                myline=line.replace('[[],[]]',begin)
                    
            elif 'alltrans=[[],[]]' in line:
                sub='[['
                for i in range(len(alltrans)):
                    items=alltrans[i]
                    for z in range(len(items)):
                        if z==len(items)-1:
                            if i==len(alltrans)-1:
                               sub+='"'+items[z]+'"]]'
                            else:
                                sub+='"'+items[z]+'"],['
                        else:
                            sub+='"'+items[z]+'",'
                myline=line.replace('[[],[]]',sub)

            elif 'i<2' in line:
                myline=line.replace('2',str(n-1))
            elif 'var shuffled = shuffle([3,4,5,6]);' in line:
                num_items=n-1
                string=''
                for i in range(num_items-no_practiceq):
                    if i==0:
                        string+=str(i+no_practiceq+1)
                    else:
                        string+=','+str(i+no_practiceq+1)
                myline=line.replace('3,4,5,6',string)
            elif 'var trialOrder =[1,2].concat(shuffled);' in line:
                string=''
                for i in range(no_practiceq):
                    if i==0:
                        string+=str(i+1)
                    else:
                        string+=','+str(i+1)
                myline=line.replace('1,2',string)
                if no_practiceq==0:
                    myline='var trialOrder=shuffled;'
            elif 'var nTrials=6' in line:
                myline=line.replace('6',str(num_items))   
            else:
                myline=line
            code.append(myline)

        # get rid of the stuff ending the script and form
        code=code[:-2]        
    
        # add the inner HTML lines

        trans_rep="document.getElementById('transX').innerHTML='One of them means '+trans_choices[X]"
        ques_rep="document.getElementById('quesX').innerHTML='Which one do you think means '+trans_choices[X]+'?'"
        foil_rep="document.getElementById('foilplayer-X').src=foil_choices[X]"
        for z in range(num_items):
            trans=trans_rep.replace('transX','trans'+str(z+1))
            trans=trans.replace('X',str(z))
            ques=ques_rep.replace('quesX','ques'+str(z+1))
            ques=ques.replace('X',str(z))
            foil=foil_rep.replace('foilplayer-X','foilplayer-'+str(z+1))
            foil=foil.replace('X',str(z))
            code.append(trans)
            code.append(ques)
            code.append(foil)

        # add back the end of the script and form
        code.append('</script>')
        code.append('</form>')
        all_experiments.append(code)


    # check what questions are in the exit survey
    exit_vars=[]
    for line in exitques:
        if 'name=' in line:
            split=line.split('name=')[1]
            try:
                var=split.split('"')[1]
            except IndexError:
                var=split.split("'")[1]
            if var not in exit_vars:
                exit_vars.append(var)
        

    # write all the experiments
    n=1
    path=os.getcwd()+'\\experiments\\'
    if not os.path.exists(path):
        os.mkdir(path)
    
    for exp in all_experiments:
        name='experiment'+str(n)+'.html'
        # write the experiment
        with open(path+name,'w') as outfile:
            for line in exp:
                outfile.write('%s\n'%line.strip('\n'))
        outfile.close()

        # write the php
        php=[]
        php_template=codecs.open(os.path.join(here,'templates','php_temp.php'),'r','utf-8')
        
        for line in php_template:
            if 'data.csv' in line:
                newline=line.replace('data','experiment'+str(n))
            else:
                newline=line
            php.append(newline)

        php_file='experiment'+str(n)+'.php'
        with open(path+php_file,'w') as outfile:
            for line in php:
                outfile.write('%s\n'%line.strip('\n'))
        outfile.close()

        # write the csv file to store responses
        csv_file='experiment'+str(n)+'.csv'
        with open(path+csv_file,'w',newline='') as outfile:
            writer=csv.writer(outfile)
            n_items=len(experiments[str(n)])
            header=[]
            for i in range(n_items):
                header.append('trans'+str(i+1))
                header.append('foil'+str(i+1))
                header.append('answer'+str(i+1))
                header.append('ReactionTime'+str(i+1))
            for var in exit_vars:
                header.append(var)
                print(var)
            writer.writerow(header)
        outfile.close()
        n+=1
