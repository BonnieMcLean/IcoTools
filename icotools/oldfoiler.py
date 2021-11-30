import csv
import os

def foiler(stimuli_list,writing_system=None):
    """Inputs are a stimuli file, containing at least the column 'form',
and if you are not using IPA, then you need a file indicating how your
writing system maps to IPA. Please use UTF-8 for your files. See https://github.com/BonnieMcLean/IcoTools for more details."""

    if writing_system==None:
        all_words=""

    words=[]
    with open(stimuli_list,"r",encoding="UTF-8") as infile:
        reader=csv.DictReader(infile)
        for row in reader:
            word=row[form]
            words.append(word)
            if writing_system==None:
                all_words=all_words+" "+word


    symbol_dict={}
    if writing_system!=None:
        with open(writing_system,"r",encoding="UTF-8") as infile:
            reader=csv.DictReader(infile)
            for row in reader:
                try:
                    symbol=row["letter"]
                    ipa=row["ipa"]
                except KeyError:
                    print("Please use the column labels 'letter', for the characters in your writing system, and 'ipa' for their IPA transcriptions.")
                symbol_dict[symbol]=ipa
        infile.close()

        letters=symbol_dict.keys()


    # figure out the distances for the ipa characters
    here=os.path.dirname(os.path.abspath(__file__))
    path=os.path.join(here,'features','ipa2hayes.txt')
    vowels={}
    consonants={}
    with open(path,"r",encoding="UTF-8") as infile:
        reader=csv.reader(infile,delimiter="\t")
        next(reader)
        for row in reader:
            ipa=row[0]
            diphthong=row[29]
            values=''.join(row[1:])
            if writing_system!=None:
                if ipa in symbol_dict.values():
                    if diphthong!='0':
                        vowels[ipa]=values
                    else:
                        consonants[ipa]=values
            else:
                if ipa in all_words:
                    if diphthong!='0':
                        vowels[ipa]=values
                    else:
                        consonants[ipa]=values           
    infile.close()

    if writing_system==None:
        letters=´list(vowels.keys())+list(consonants.keys())


    # function for calculating difference between two value sets
    def value_diff(a,b):
        return sum ( a[i] != b[i] for i in range(len(a)) )

    # calculate distances between all possible pairs of ipa characters
    distances={}
    # first for vowels
    for item in vowels.keys():
        to_compare=list(vowels.keys())
        to_compare.remove(item)
        for letter in to_compare:
            diff=value_diff(vowels[item],vowels[letter])
            try:
                distances[item][0].append(letter)
                distances[item][1].append(diff)
            except KeyError:
                distances[item]=[[letter],[diff]]

    # then consonants
    for item in consonants.keys():
        to_compare=list(consonants.keys())
        to_compare.remove(item)
        for letter in to_compare:
            diff=value_diff(consonants[item],consonants[letter])
            try:
                distances[item][0].append(letter)
                distances[item][1].append(diff)
            except KeyError:
                distances[item]=[[letter],[diff]]  

    # figure out the top three most distant sounds for each sound
    for key in distances.keys():
        subs=[]
        for i in range(3):
            max_distance=max(distances[key][1])
            index=distances[key][1].index(max_distance)
            letter=distances[key][0][index]
            subs.append(letter)
            distances[key][1].pop(index)
            distances[key][0].pop(index)
        distances[key]=subs

    # Now time to make the foil words

    # the words are in the list called 'words'


            

    # arrange the letters from the longest to the shortest: this is the order you should change stuff
    letters=sorted(letters,key=len)
    letters.reverse()
