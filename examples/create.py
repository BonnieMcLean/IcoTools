import icotools

# mp4 stimuli, guessing experiments

icotools.guesser('mp4stimuli_randomfoils.csv','gestures_custom.csv')
icotools.guesser('mp4stimuli_randomfoils.csv','gestures_default.csv')

icotools.guesser('mp4stimuli_randomfoils.csv','JSL_custom.csv')
icotools.guesser('mp4stimuli_randomfoils.csv','JSL_default.csv')

# mp4 stimuli, rating experiments

icotools.rater('mp4stimuli_randomfoils.csv','gestures_custom.csv')
icotools.rater('mp4stimuli_randomfoils.csv','gestures_default.csv')

icotools.rater('mp4stimuli_randomfoils.csv','JSL_custom.csv')
icotools.rater('mp4stimuli_randomfoils.csv','JSL_default.csv')

# mp3 stimuli, guessing experiments

icotools.guesser('mp3stimuli_oppositefoils.csv','Korean_custom.csv')
icotools.guesser('mp3stimuli_oppositefoils.csv','Korean_default.csv')

icotools.guesser('mp3stimuli_oppositefoils.csv','Nonwords_default.csv')

# mp3 stimuli, rating experiments

icotools.rater('mp3stimuli_oppositefoils.csv','Korean_custom.csv')
icotools.rater('mp3stimuli_oppositefoils.csv','Korean_default.csv')


icotools.rater('mp3stimuli_oppositefoils.csv','Nonwords_default.csv')
