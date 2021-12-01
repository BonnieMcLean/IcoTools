import csv
import os
import numpy as np
import re
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
    specified=[]
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
                    substitutions[letter]=sub.split("|")
                    specified.append(letter)
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
    path=os.path.join(here,'features','phoible-segments-features.tsv')
    with open(path,"r",encoding="UTF-8") as infile:
        next(infile)
        reader=csv.reader(infile,delimiter="\t")
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
                        print("Your sound "+sound+" is missing from the feature table. You can manually add it to the feature table by editing the file phoible-segments-features.tsv in the features folder in your icotools folder")
                        raise SystemExit
                    try:
                        two=features[item]
                    except KeyError:
                        print("ERROR!")
                        print("Your sound "+item+" is missing from the feature table. You can manually add it to the feature table by editing the file phoiblefeatures.txt in the features folder in your icotools folder")
                        raise SystemExit

                    # set the difference between the two sounds to zero
                    diff=0
                    # weight differences in length and voicing a little less
                    length_voicing_cols=[3,4,29]
                    for i in range(len(one)):
                        if one[i]!=two[i]:
                            if one[i]=="0" or two[i]=="0":
                                diff+=.25
                            else:
                                if i in length_voicing_cols:
                                    diff+=.5
                                else:
                                    diff+=1

                    try:
                        distances[sound][0].append(item)
                        distances[sound][1].append(diff)
                    except KeyError:
                        distances[sound]=[[item],[diff]]
        else:
            for sound in group:
                subs=list(group)
                subs.remove(sound)
                substitutions[sound]=subs
    # figure out the top three biggest distances, and add sounds with those distances to the substitutions dictionary until you have at least 3 subs for each sound
    distance_record=[]
    for key in distances.keys():
        # sort distances from highest to lowest
        dists=sorted(distances[key][1],reverse=True)
        subs=[]
        i=0
        while len(subs)<3:
            indexes=np.where(np.array(distances[key][1])==dists[i])[0]
            for z in indexes:
                thing=distances[key][0][z]
                if thing not in subs:
                    subs.append(thing)
                    distance_record.append((key,thing,dists[i]))
            i+=1
        if key not in substitutions.keys():
            substitutions[key]=subs

    ordered_subs=sorted(list(substitutions.keys()),key=len,reverse=True)

    # make the foils
    outlines=[]
    with open(stimuli,'r',encoding="UTF-8") as infile:
        reader=csv.DictReader(infile)
        headers=reader.fieldnames
        headers.append("foils")
        outlines.append(headers)
        for row in reader:
            word=row["form"]
            # first check if it's reduplicated
            if len(word)%2==0:
                if word[0:int(len(word)/2)]==word[int(len(word)/2):]:
                    # if it's reduplicated, let's unreduplicate it
                    word=word[0:int(len(word)/2)]
            # then make the substitutions
            original=str(word)
            # get a list of unique sounds to replace
            sounds=[]
            for key in ordered_subs:
                if key in word:
                    sounds.append(key)
                    word=word.replace(key,"")

            # subdivide the words into those sounds
            # first split the word into characters
            wordsplit=list(original)

            # then go through and join them back together if they belong to a bigraph
            substitute=[]
            i=0
            while i<len(wordsplit):
                current=wordsplit[i]
                try:
                    next_one=wordsplit[i+1]
                except IndexError:
                    next_one=""
                if current+next_one in sounds:
                    substitute.append(current+next_one)
                    i=i+2
                else:
                    substitute.append(current)
                    i=i+1
            foil1=list(substitute)
            foil2=list(substitute)
            foil3=list(substitute)
            original=list(substitute)
            
            # replace each of the sounds
            for i in range(len(substitute)):
                key=original[i]
                subs=list(substitutions[key])

                if len(subs)<3:
                    if len(subs)==1:
                        sub=subs.pop()
                        foil1[i]=sub
                        foil2[i]=sub
                        foil3[i]=sub
                    else:
                        index=randint(0,1)
                        sub1=subs.pop(index)
                        sub2=subs.pop()
                        foil1[i]=sub1
                        foil2[i]=sub1
                        foil3[i]=sub2
                else:
                    index=randint(0,len(subs)-1)
                    sub=subs.pop(index)
                    foil1[i]=sub
                    index=randint(0,len(subs)-1)
                    sub=subs.pop(index)
                    foil2[i]=sub
                    index=randint(0,len(subs)-1)
                    sub=subs.pop(index)
                    foil3[i]=sub
            
            line=list(row.values())
            foil1="".join(foil1)
            foil2="".join(foil2)
            foil3="".join(foil3)
            line[-1]=foil1+"|"+foil2+"|"+foil3
            outlines.append(line)

            # check you didn't miss any characters in your letters file
            for char in original:
                found=False
                for key in substitutions.keys():
                    if char in key:
                        found=True
                if not found:
                    print("WARNING! The letter "+char+" in the word "+original+" was not found in your letters file, so it has not been replaced in the foils!")
                    print("We recommend you add this letter to the letters file and rerun this program before proceeding.")
        infile.close()

                    
    # now write the file
    with open(stimuli.strip('.csv')+"_oppfoils.csv","w",encoding="UTF-8",newline="") as outfile:
        writer=csv.writer(outfile)
        for line in outlines:
            writer.writerow(line)
    outfile.close()

    # also write the substitutions
    with open("substitutions.csv","w",encoding="UTF-8",newline="") as outfile:
        writer=csv.writer(outfile)
        writer.writerow(("letter","substitution","distance"))
        outlines=[]
        for item in distance_record:
            letter=item[0]
            if letter in specified:
                if (letter,"|".join(substitutions[letter]),"not calculated (user-specified substitution)") not in outlines:
                    outlines.append((letter,"|".join(substitutions[letter]),"not calculated (user-specified substitution)"))
            else:
                outlines.append(item)
        for item in outlines:
            writer.writerow(item)
    outfile.close()



        
