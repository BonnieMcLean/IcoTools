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

    return(experiments)



def rater(stimuli_list,control_file):
    """Makes rating tasks, see https://github.com/BonnieMcLean/IcoTools for the format of the stimuli list and control file"""


    instructions="""
    <div id="about">
    <h3 style="text-align: center">About</h3>
    <p>Some words seem to 'fit' their meanings. For example, consider the English words <i>wiggle</i>, <i>jiggle</i>, and <i>wriggle</i>.</p>
    <p>We have an intuitive sense of the meanings of these words, because there is a resemblance between the words and their meanings.</p>
    <p>Even people who do not speak any English can get a sense of the meaning of these words.</p>
    <p>Words like <i>walk</i> and <i>run</i> on the other hand are not so intuitive; people who do not know any English would not be able to guess what these words mean.</p>
    <p>In this task, you will listen to some Japanese words, and we will tell you their meanings. You will then be asked to judge whether there is
    a resemblance between the word and its meaning. 
    </p>
    <p><strong>Criteria for participation</strong></p>
    <p>For your judgments to be unbiased, it is very important that you do NOT know any Japanese. If you do know Japanese, we kindly ask that you do not participate in this study.</p>
    <p>Since the task requires you to listen to the words, you will need to complete it in a quiet place using headphones. We will check at the beginning of the task that you are using headphones, so please make sure to use them as participants who do not use headphones will not be able to complete the task.</p> 
    <p>Participation is completely voluntary, anonymous and confidential. If you meet the above criteria and agree to participate, please click 'Participate'.</p>
    </div>
    """

    exit_ques="""
    <p>This is the end of the task. However, before you submit your answers we need to collect some information from you. Kindly fill in the following:</p>
    <p><strong>Native Language*:</strong><input type="text" name="lang" required></p>
    <p><strong>Other languages you understand:</strong><input type="text" name="otherlang"></p>
    <p><strong>For our feedback, please also describe the TASK you were performing*:</strong></p>
    <p><input type="text" name="taskdesc" size="80"></p>
    <p>*Required</p>
    """

    submit_message="""
    <p>Thank you for participating in this research!</p>
    """

    # read in the information from the control file
    control={}
    with open(control_file,'r',encoding='UTF-8') as infile:
        reader=csv.reader(infile)
        for row in reader:
            key=row[0]
            value=row[1]
            control[key]=value
    try:
        media_source=control['media_source']
        media_type=control['media_type']
        language=control['language']
        instructions_html=control['instructions_html']
        exitques_html=control['exitques_html']
        submit_html=control['submit_html']
        headphone_check=control['headphone_check']
        words_per_exp=int(control['words_per_exp'])
    except KeyError:
        print('Your control file is not formatted correctly. See https://github.com/BonnieMcLean/IcoTools for the correct format.')
    try:
        muted_vids=control['muted_vids']
    except KeyError:
        pass
    if instructions_html=='default':
        instructions=instructions.replace("Japanese",language)
    if exitques_html=='default':
        exitques=exit_ques
        exitques_labels=["NativeLang","OtherLangs","TaskDesc"]
    else:
        exitques=exitques_html
        try:
            exitques_labels=control["exitques_labels"]
            exitques_labels=exitques_labels.split(",")
        except KeyError:
            print("Please provide labels for your exit questions. See https://github.com/BonnieMcLean/IcoTools for more information.")
    if submit_html!="default":
        submit_message_raw=codecs.open(submit_html,'r','utf-8')
        submit_message_l=[]
        for line in submit_message_raw:
            submit_message_l.append(line)
        submit_message=' '.join(submit_message_l)
        submit_message=submit_message.replace('"',"'")
    
    if media_type!='mp3' and media_type!='mp4':
        print('Please enter a valid media type. Valid media types are mp3 or mp4.')
        return

    # call balancer to make the experiments
    experiments_raw=balancer(stimuli_list,words_per_exp)
    experiments={}
    for i in range(len(experiments_raw)):
        experiments[str(i+1)]=experiments_raw[i]

    # make experiments list

    filename=stimuli_list.strip('.csv')+'_experiments.csv'
    with open(filename,'w',newline='') as outfile:
        writer=csv.writer(outfile)
        writer.writerow(('experiment','item_type','form','meaning','hypothesis'))
        for exp in experiments:
            stuff=experiments[exp]
            for word in stuff:
                form=word[0]
                meaning=word[1]
                hypothesis=word[2]
                item_type=word[3]
                writer.writerow((exp,item_type,form,meaning,hypothesis))
    outfile.close()

    # get together code for rating tasks

    intro_code=[]
    trial_code=[]
    outro_code=[]
    here = os.path.dirname(os.path.abspath(__file__))
    if media_type=='mp4':
        template=codecs.open(os.path.join(here,'templates','ratings_mp4.html'),'r','utf-8')
    else:
        template=codecs.open(os.path.join(here,'templates','ratings_mp3.html'),'r','utf-8')
    
    section=1
    for line in template:
        if section==1:
            # intro code
            intro_code.append(line)
            if '<!---TRIAL START!---->' in line:
                section+=1
        elif section==2:
            # real test items
            trial_code.append(line)
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

    if ".html" in instructions_html:
        instructions_all=codecs.open(instructions_html,'r','utf8')      
        instructions_l=[]
        for line in instructions_all:
            instructions_l.append(line)
    else:
        instructions_l=[instructions]


    # split intro code into two by line INSTRUCTIONS
    for i in range(len(intro_code)):
        if 'INSTRUCTIONS' in intro_code[i]:
            index=i
    intro_code_1=intro_code[:index]
    intro_code_2=intro_code[index+1:]
    intro_code=intro_code_1+instructions_l+intro_code_2

    # add exit quest to the outro code
    if ".html" in exitques_html:
        exitques=codecs.open(os.path.join(here,exitques_html),'r','utf-8')
        exit_l=[]
        for line in exitques:
            exit_l.append(line)
    else:
        exit_l=[exitques]

    # split outro code into two by line EXIT QUESTIONS
    for i in range(len(outro_code)):
        if 'OUTRO_QUESTIONS' in outro_code[i]:
            index=i

    outro_code_1=outro_code[:index]
    outro_code_2=outro_code[index+1:]
    outro_code=outro_code_1+exit_l+outro_code_2


    all_experiments=[]
    for exp in experiments:
        alltrans=[]
        code=[]
        for item in intro_code:
            if 'experimentX.php' in item:
                code.append(item.replace('X',exp))
            else:
                code.append(item)

        trials=experiments[exp]

        n=1
        for trial in trials:
            trans=trial[1].upper().split('|')
            alltrans.append(trans)
            for line in trial_code:
                if '<div id="trial1" class="trialDiv">' in line:
                    myline=line.replace('trial1','trial'+str(n))
                elif "id='trans1'" in line:
                    myline=line.replace('trans1','trans'+str(n))
                elif 'SOUNDFILE' in line:
                    word=trial[0]
                    myline=line.replace('SOUNDFILE',media_source+word+'.mp3')
                elif 'name="chosentrans1"' in line:
                    myline=line.replace('chosentrans1','chosentrans'+str(n))
                elif 'name="q1"' in line:
                    myline=line.replace('q1','q'+str(n))
                elif "id='player1'" in line:
                    myline=line.replace('player1','player'+str(n))
                elif 'options1' in line:
                    myline=line.replace('options1','options'+str(n))
                elif 'reactionTime1' in line:
                    myline=line.replace('reactionTime1','reactionTime'+str(n))
                    myline=myline.replace('rt1','rt'+str(n))
                else:
                    myline=line
                code.append(myline)

            n+=1
        
        # now time to make the outro code
        for line in outro_code:
            if 'alltrans=[[],[]]' in line:
                sub='[['
                for i in range(len(alltrans)):
                    items=alltrans[i]
                    for z in range(len(items)):
                        if z==len(items)-1:
                            if i==len(alltrans)-1:
                               sub+='"'+items[z].upper()+'"]]'
                            else:
                                sub+='"'+items[z].upper()+'"],['
                        else:
                            sub+='"'+items[z].upper()+'",'
                myline=line.replace('[[],[]]',sub)

            elif 'i<2' in line:
                myline=line.replace('2',str(n-1))
            elif 'var shuffled = shuffle([3,4,5,6]);' in line:
                num_items=n-1
                string=''
                for i in range(num_items-2):
                    if i==0:
                        string+=str(i+3)
                    else:
                        string+=','+str(i+3)
                myline=line.replace('3,4,5,6',string)
            elif 'var nTrials=6' in line:
                myline=line.replace('6',str(num_items))   
            else:
                myline=line
            code.append(myline)

        # get rid of the stuff ending the script and form
        code=code[:-2]

        # add the inner HTML lines
        
        trans_rep="document.getElementById('transX').innerHTML='<p>Listen to the "+language+" word below.</p><p>It means '+trans_choices[X]+'.</p>'"
        for z in range(num_items):
            trans=trans_rep.replace('transX','trans'+str(z+1))
            trans=trans.replace('X',str(z))
            code.append(trans)

        # add back the end of the script and form
        code.append('</script>')
        code.append('</form>')
        all_experiments.append(code)

    # write all the experiments

    path=os.getcwd()+'\\experiments\\'
    if not os.path.exists(path):
        os.mkdir(path)

    n=1
    for exper in all_experiments:
        # write the html
        name='experiment'+str(n)+'.html'
        with open(path+name,'w') as outfile:
            for line in exper:
                outfile.write('%s\n'%line.strip('\n'))
        outfile.close()

        # write the php
        php=[]
        php_template=codecs.open(os.getcwd()+'\\templates\\php_temp.php','r','utf-8')
        for line in php_template:
            if 'data.csv' in line:
                newline=line.replace('data','experiment'+str(n))
            elif "Print a message for them" in line:
                newline='print("'+submit_message+'");'
            else:
                newline=line
            php.append(newline)

        path_php=os.getcwd()+'\\experiments\experiment'+str(n)+'.php'
        
        with open(path_php,'w') as outfile:
            for line in php:
                outfile.write('%s\n'%line.strip('\n'))
        outfile.close()


        # write the csv file to store responses
        path_csv=os.getcwd()+'\\experiments\experiment'+str(n)+'.csv'
        with open(path_csv,'w',newline='') as outfile:
            writer=csv.writer(outfile)
            n_items=len(experiments[str(n)])
            header=[]
            for i in range(n_items):
                header.append('t'+str(i+1))
                header.append('a'+str(i+1))
                header.append('rt'+str(i+1))

            for label in exitques_labels:
                header.append(label)

            writer.writerow(header)
        outfile.close()
        n=n+1

    n+=1

    
