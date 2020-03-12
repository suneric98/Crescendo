# Crescendo

A Spotify application analyzing Spotify top songs. This application focuses on identifying what makes a song popular and providing visualizations to show information about them.

## Log of activities

### 2/15

+ Eric: got dataset, got features from Spotify
+ Kathy: data exploration, changed types of dataset
+ Chris: data exploration and cleaning; created variations of dataset to 

### 2/29

+ Eric: made viz with selections for artists and songs showing rank over time,
  performed basic data exploration
+ Eric: got artists data and did basic exploration with it
+ Kathy: built a linear regression model to predict the rank of a song based on
the number of streams
+ Chris: clustered songs in dataset based on scaled continuous features; wrote functions to faciliate access of artists and songs in each cluster

### 2/29 TODO

+ Eric: clustering stuff: try to group songs/artists by genre using artist
  genre
  + Need to group genres so we don't have 300+ genres

### 3/7

+ Eric: grouped artist data together, began working on regression prediction for
number of days a song remains in top chart
+ Chris: modularized clustering notebook file

### 3/7 TODO

+ Eric: improve regression model for num of days

### 3/11 Meeting

Agenda

+ Everyone update README
+ No presentation Saturday!
+ What has everyone done: Clustering, LR for trend, regression for day
  prediction
+ Work TODO
  + Finish clustering and stuff soon
  + Improve ML predictions

### 3/14

+ Chris: wrote functions to assign genres to songs in each cluster based on genres of artists in cluster; experimented with various labeling methods

### TODO:

+ for line viz add smoothing for jumps in time
  + Add legend to viz
+ figure out how exactly supervised algo will work (in progress)
+ possible feature for predict: release date of album/new song