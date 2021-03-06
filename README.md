# Crescendo

A Spotify application analyzing Spotify top songs. This application focuses on identifying what makes a song popular and providing visualizations to show information about them.

## Log of activities

### 2/15

+ Eric: got dataset, got features from Spotify
+ Kathy: data exploration, changed types of dataset
+ Chris: data exploration and cleaning
+ Angela: data exploration

### 2/29

+ Eric: made viz with selections for artists and songs showing rank over time,
  performed basic data exploration
+ Eric: got artists data and did basic exploration with it
+ Kathy: Started building a linear regression model to predict the rank of a song based on the number of streams.
+ Chris: clustered songs in dataset based on scaled continuous features; wrote functions to faciliate access of artists and songs in each cluster
+ Angela: Made exploration data visualization (2-D scatterplot, 3-D scatterplot, bar graph).  

### 2/29 TODO

+ Eric: clustering stuff: try to group songs/artists by genre using artist
  genre
  + Need to group genres so we don't have 300+ genres

### 3/7

+ Eric: grouped artist data together, began working on regression prediction for
number of days a song remains in top chart
+ Chris: modularized clustering notebook file
+ Angela: Gained knowledge about clustering KNN, Kmeans, neural networks, linear regression.
+ Kathy: Converted column types to floats and integers and created a new csv file.
Continued to build a linear regression model to predict the rank of a song based on the number of streams.


### 3/7 TODO

+ Eric: improve regression model for num of days
+ Chris: ran PCA on features and clustered on resulting data

### 3/14

+ Chris: wrote functions to assign genres to songs in each cluster based on genres of artists in cluster; experimented with various labeling methods
+ Angela: Developed understanding of the models used for rank predication. Also attended D3 onboarding workshop.
+ Kathy: Tested the linear regression models by inputting different songs and predicting the rank.

## Post Break Journal

### 4/4

+ Eric: made neural network to predict the number of days song stays in top chart
+ Chris: developed regression and classification models to predict how long a song stays in the top charts
+ Angela: Attended supervised learning workshop.
+ Kathy: Built a polynomial regression model to predict the rank of a song based on the number of streams

### 4/11

+ Eric: Edited chris' model to predict "grouping" of how long song stays in top chart,
  didn't get great results
+ Chris: for classification models, attempted class balancing via oversampling/undersampling but still unable to beat baseline accuracy;
implemented boosting methods to increase accuracy with little improvement
+ Angela: found new dataset that includes more in-depth features, such as genre labelling and artist popularity.
+ Kathy: Developed a linear regression model with the log-transformed rank. Continued to explore polynomial regression.


### 4/18

+ Eric: began flask app for visualizations
+ Chris: finalized PCA clustering on songs
+ Kathy: Updated the linear regression model with the log-transformed rank.
Updated visualizations of the model to include positive rank values.

### 4/25

+ Eric: continued implementing flask app with work done over the semester,
  planning to have a vis for Kathy's work
+ Angela: trained a KNN algorithm to predict the song’s genre with the given features in the new kaggle dataset;
preprocessed the kaggle dataset to create main groupings for genres, as dataset has overlap in genre labelling.
+ Chris: started d3 visualization for song clustering results
+ Kathy: Tested the linear regression model with log-transformed rank by predicting the ranks of different songs. Finalized visualizations of the model.

### 4/25

+ Chris: clustered artists based on features derived from their songs