import icotools

# mp4 stimuli, guessing experiments

icotools.guesser('02-mp4stimuli_randomfoils.csv','gestures_custom.csv')
icotools.guesser('02-mp4stimuli_randomfoils.csv','gestures_default.csv')

icotools.guesser('02-mp4stimuli_randomfoils.csv','JSL_custom.csv')
icotools.guesser('02-mp4stimuli_randomfoils.csv','JSL_default.csv')

# mp4 stimuli, rating experiments

icotools.rater('02-mp4stimuli_randomfoils.csv','gestures_custom.csv')
icotools.rater('02-mp4stimuli_randomfoils.csv','gestures_default.csv')

icotools.rater('02-mp4stimuli_randomfoils.csv','JSL_custom.csv')
icotools.rater('02-mp4stimuli_randomfoils.csv','JSL_default.csv')

# mp3 stimuli, guessing experiments

icotools.guesser('01-mp3stimuli_oppositefoils.csv','Korean_custom.csv')
icotools.guesser('01-mp3stimuli_oppositefoils.csv','Korean_default.csv')

icotools.guesser('01-mp3stimuli_oppositefoils.csv','Nonwords_default.csv')

# mp3 stimuli, rating experiments

icotools.rater('01-mp3stimuli_oppositefoils.csv','Korean_custom.csv')
icotools.rater('01-mp3stimuli_oppositefoils.csv','Korean_default.csv')


icotools.rater('01-mp3stimuli_oppositefoils.csv','Nonwords_default.csv')

# image stimuli, guessing and rating experiments
icotools.guesser('02-imagestimuli_randomfoils.csv','images_custom.csv')
icotools.rater('02-imagestimuli_randomfoils.csv','images_custom.csv')
