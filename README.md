# Google Store APP

## Purpose
I am going to use a data set about google store apps from:  https://www.kaggle.com/lava18/google-play-store-apps
The csv file is also in the zip file.
The relation between an app and genre can be M2M because one app can have more than one genre and many app can have the same genre.
The django app will show the size, overview, install timew,type ,genre,price,rating,version of the app in google store.
 
## Data set
https://www.kaggle.com/lava18/google-play-store-apps
## Data model
Seven tables in all.
The relation between App and Genre is many to many.

Here's the data model:
![Data Model](https://github.com/wowwh/SI664_FinalProject/blob/master/static/img/diagram.png?raw=true "Data Model")
## Package Dependencies
