# General overview

Icotools is a [python package](https://pypi.org/project/icotools/), to install it, use `pip install icotools`.

Icotools comes with two functions:

- `icotools.guesser('stimuli.csv','controlfile.csv')`
- `icotools.rater('stimuli.csv','controlfile.csv')`

The guesser function makes guessing experiments, where participants are given a meaning and have to match the meaning to the correct stimulus, in a two alternative forced-choice paradigm. Stimuli can be either MP3 files, MP4 files, or images. A demo is available [here](https://honestcookingblog.com/experiments/experiment1.html#). For more about the guessing experiments and their different variations, see the [instructions for guessing experiments](#Instructions-for-guessing-experiments).

The ratings function makes rating experiments, where participants are presented with stimuli (either MP3 files, MP4 files, or images) and their meanings, and asked to rate on a 7-point scale whether they think there is a resemblance between the stimulus and its meaning, from 0 'No resemblance' to 6 'Strong resemblance'. The exact labels used can be modified as desired. See [instructions for rating experiments](#Instructions-for-rating-experiments) for more information.

Each function takes a list of stimuli (stimuli.csv) and a control file (control.csv) as inputs, and produces a folder of html experiments to collect measures of iconicity on those items. For each experiment, three files are produced--a html file, a php file, and a csv file. Once you upload all these files to your server, and share the link to the html experiments with participants, as participants complete your study, their answers (as well as their reaction times for each item, and a record of which translation/foil was presented to them for each item) will be written to the csv file on your server (by the php). 

# Instructions for guessing experiments

You can either 

(a) make guessing experiments where the foils for each item are specified, or   
(b) make guessing experiments where the foils for each item are randomly chosen from all the items available, with the option to specify particular item-foil pairings which should *not* be used.

**Format for the control file**:

It should be a csv file with two columns, the first column contains variable names and the second column contains their values.

|Col1             |Col2                                                                                      |
|-----------------|------------------------------------------------------------------------------------------|
|media_source     |link to location of media files                                                           |
|media_type       |media format (either mp4, mp3, jpg, jpeg, png)                                            |                                                                           |
|muted_vids       |(optional) either 'y' or 'n' if you want to mute the audio in the videos                  |                                                                             |
|headphone_check  |do you want to include a headphone check at the start of the experiment--either 'y' or 'n'|                                                                        |
|instructions_html|either 'default' or provide filename to your own html instructions                        |                                                                       |
|exitques_html    |either 'default' or provide filename to your own html exit questions                      |                                                                        |
|words_per_exp    |roughly how many words would you like to test per experiment (inc. practice questions)    |                                                                        |

**Format for the stimuli file**
It should be a csv file with (up to) 6 columns. The first three columns are required, but the last three are optional. Having extra columns (with stuff not relevant to the experiments) also doesn't matter.

|form                                                                                                                                                                                                                      |item                                                                                                                                |meaning                                   |foils                                                                                                                                   |no_foils                                                                                                                                      |iconic                                                                                                                                                                 |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|the form to be tested--this should correspond to the name of your media files, e.g. if the form is honnori the media file should be called honnori.mp3 or honnori.mp4 etc. (depending on what you put in the control file)|either 'practice' (if it's a practice item), 'control' (if it's a control item) or 'trial' (if it's one of the items you're testing)|one or more translations, separated by \\||the names of items you want to use as foils. These should match their media file names (as for the form column), and be separated by \\||the names of items you don't want to use as foils. These should match their media file names (as for the form column), and be separated by \\||if you want to have a roughly equal number of possibly iconic vs possibly not iconic words in each experiment, indicate your hypothesis about iconicity 'y' or 'n' here|

Items marked 'practice' will be included in every experiment, at the start of the experiment. Items marked 'control' will be included in every experiment, but randomly distributed throughout the experiment (the order of presentation of stimuli is different for each participant). Items marked 'trial' will only be included in one experiment (also in a random order), and are the items you are actually testing.

See examples in the example folder.

# Instructions for rating experiments

COMING SOON
