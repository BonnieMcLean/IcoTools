import csv
import os
import numpy as np
from random import randint

def foiler(stimuli,letters):
    """Inputs are a stimuli file, containing at least the column 'form', and a file
indicating how your writing system maps to IPA, and which sounds can be freely swapped with
each other (as initials, medials, finals etc.). Please use UTF-8 encoding for your files.
See https://github.com/BonnieMcLean/IcoTools for more details."""

    substitutions={}

    # read in the sounds in their groups
    subgroups={}
    i=-1
    currentgroup=None
    ipa2letter={}
    with open(letters,'r',encoding='utf-8') as infile:
        reader=csv.DictReader(infile)
        for row in reader:
            try:
                letter=row['letter']
                group=row['group']
            except KeyError:
                print("Please use the correct headings for your letters file. They should be 'letter','ipa' (if letters are not IPA), 'group' (for the substitution groups) and 'substitute' (if you want to specify your own substitutes).")
            try:
                ipa=row['ipa']
            except KeyError:
                ipa=letter
            try:
                sub=row['substitute']
                if sub!="":
                    substitutions[letter]=[sub]
            except KeyError:
                pass
            try:
                if letter not in subgroups[group]:
                    subgroups[group].append(letter)
            except KeyError:
                subgroups[group]=[letter]
            ipa2letter[ipa]=letter
    infile.close()
    subgroups=list(subgroups.values())
    
    # get their feature values
    features={}
    here=os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(here,'features','phoiblefeatures.txt')
    with open(path,"r",encoding="UTF-8") as infile:
        next(infile)
        reader=csv.reader(infile)
        for row in reader:
            ipa=row[0]
            if ipa in list(ipa2letter.keys()):
                letter=ipa2letter[ipa]
                features[letter]=''.join(row[1:])
    infile.close()
    # figure out the 3 most distant sounds for each sound
    # if there are 4 sounds or less then you don't need to do this
    distances={}
    for group in subgroups:
        if len(group)>4:
            for sound in group:
                compare=[]
                for i in group:
                    compare.append(i)
                compare.remove(sound)
                for item in compare:
                    try:
                        one=features[sound]
                    except KeyError:
                        print("ERROR!")
                        print("Your sound "+sound+" is missing from the feature table. You can manually add it to the feature table by editing the file phoiblefeatures.txt in the features folder in your icotools folder")
                        raise SystemExit
                    try:
                        two=features[item]
                    except KeyError:
                        print("ERROR!")
                        print("Your sound "+item+" is missing from the feature table. You can manually add it to the feature table by editing the file phoiblefeatures.txt in the features folder in your icotools folder")
                        raise SystemExit

                    # set the difference between the two sounds to zero
                    diff=0
                    for i in range(len(one)):
                        if one[i]!=two[i]:
                            if one[i]=="0" or two[i]=="0":
                                diff+=.25
                            else:
                                diff+=1

                    try:
                        distances[sound][0].append(item)
                        distances[sound][1].append(diff)
                    except KeyError:
                        distances[sound]=[[item],[diff]]
        else:
            for sound in group:
                subs=group
                subs.remove(sound)
                substitutions[sound]=subs
                
    # figure out the top three biggest distances, and add sounds with those distances to the substitutions dictionary until you have at least 3 subs for each sound
    for key in distances.keys():
        dists=sorted(distances[key][1],reverse=True)
        subs=[]
        i=0
        while len(subs)<3:
            indexes=np.where(np.array(distances[key][1])==dists[i])[0]
            for z in indexes:
                thing=distances[key][0][z]
                if thing not in subs:
                    subs.append(thing)
            i+=1
        if key not in substitutions.keys():
            substitutions[key]=subs

    ordered_subs=sorted(list(substitutions.keys()),key=len,reverse=True)
    

    # make the foils
    outlines=[]
    with open(stimuli,'r',encoding="UTF-8") as infile:
        reader=csv.DictReader(infile)
        headers=reader.fieldnames
        headers.append("foil")
        outlines.append(headers)
        for row in reader:
            word=row["form"]
            # first check if it's reduplicated
            if len(word)%2==0:
                if word[0:int(len(word)/2)]==word[int(len(word)/2):]:
                    # if it's reduplicated, let's unreduplicate it
                    word=word[0:int(len(word)/2)]
            # then make the substitutions
            foil1=str(word)
            foil2=str(word)
            foil3=str(word)
            original=str(word)
            for key in ordered_subs:
                if key in word:
                    subs=list(substitutions[key])
                    if len(subs)<3:
                        if len(subs)==1:
                            foil1=foil1.replace(key,subs[0])
                            foil2=foil2.replace(key,subs[0])
                            foil3=foil3.replace(key,subs[0])
                        else:
                            if randint(1,2)==1:
                                foil1=foil1.replace(key,subs[0])
                                foil2=foil2.replace(key,subs[1])
                                foil3=foil3.replace(key,subs[0])
                            else:
                                foil1=foil1.replace(key,subs[1])
                                foil2=foil2.replace(key,subs[0])
                                foil3=foil3.replace(key,subs[1])     
                    else:
                        index=randint(0,len(subs)-1)
                        sub=subs.pop(index)
                        foil1=foil1.replace(key,sub)
                        index=randint(0,len(subs)-1)
                        sub=subs.pop(index)
                        foil2=foil2.replace(key,sub)
                        index=randint(0,len(subs)-1)
                        sub=subs.pop(index)
                        foil3=foil3.replace(key,sub)
                    word=word.replace(key,'')
            line=list(row.values())
            line[-1]=foil1+"|"+foil2+"|"+foil3
            outlines.append(line)
        infile.close()

                    
    # now write the file
    with open(stimuli.strip('.csv')+"opp_foils.csv","w",encoding="UTF-8",newline="") as outfile:
        writer=csv.writer(outfile)
        for line in outlines:
            writer.writerow(line)
    outfile.close()

    # also write the substitutions
    with open("substitutions.csv","w",encoding="UTF-8",newline="") as outfile:
        writer=csv.writer(outfile)
        writer.writerow(["sound","substitutions"])
        for key in substitutions:
            writer.writerow([key,"|".join(substitutions[key])])
    outfile.close()



        
