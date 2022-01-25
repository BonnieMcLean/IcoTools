# specify the location of the folder with your experiment results, the
# number of experiments that you have, and the location of your summary csv file 
# (which contains the details of items in every experiment) here
file_location <- "https://honestcookingblog.com/experiments"
n_experiments <- 6
info <- read_csv("control_guessing.csv")

# code to join all experiment results together

# start with first experiment
experiments <- read_csv(paste(file_location,"/experiment1.csv",sep=""))
experiments%>%
  mutate(experiment=1)->experiments
# do the same for all the other experiments you have, progressively joining them together each time
for(i in 2:n_experiments){
  next_experiment <-read_csv(paste("https://honestcookingblog.com/experiments/experiment",as.character(i),".csv",sep=''))
  next_experiment%>%
    mutate(experiment=i)->next_experiment
  experiments <- full_join(experiments,next_experiment)
}

# Figure out what the last reaction time column is
last_RT <- tail(colnames(select(experiments,contains("rt"))),1)
# convert to tidy data
experiments%>%
  # in case there are any double submissions
  unique()%>%
  pivot_longer(cols=t1:last_RT,names_to=c(".value","trial"),names_pattern="([A-Za-z]+)(\\d+)")%>%
  rename(trans=t,response=a,foil=f)%>%
  # get rid of NAs -- for the experiments that have less trials
  filter(!(is.na(trans)))->experiments
# add identifiers (in the format word_MEANING) for the trials -- this is important in case you have homonyms in your data. I just use the first translation in the meaning column to make these identifiers.

info%>%
  rowwise()%>%
  mutate(identifier=paste(form,str_split(meaning,"\\|")[[1]][1],sep="_"))%>%
  select(experiment,trial,form,identifier)->info
info$trial <- as.character(info$trial)
# join to experiment data
experiments%>%
  left_join(info)->experiments

# grade responses
grade_responses <- function(trial,response){
  trial <- as.numeric(trial)
  if(trial%%2==1&response=="A"){return("correct")}
  else if(trial%%2==0&response=="B"){return("correct")}
  else{return("incorrect")}
}

experiments%>%
  rowwise()%>%
  mutate(grade=grade_responses(trial,response))->experiments

write_csv(experiments,"guessingres.csv")
