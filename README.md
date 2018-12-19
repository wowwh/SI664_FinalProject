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


## Site Overview
![Site Overview](https://github.com/wowwh/SI664_FinalProject/blob/master/static/img/site.png?raw=true "Site Overview")



## Package Dependencies
certifi==2018.10.15
chardet==3.0.4
coreapi==2.3.3
coreschema==0.0.4
defusedxml==0.5.0
Django==2.1.2
django-allauth==0.38.0
django-cors-headers==2.4.0
django-crispy-forms==1.7.2
django-filter==2.0.0
django-rest-auth==0.9.3
django-rest-swagger==2.2.0
django-test-without-migrations==0.6
djangorestframework==3.9.0
idna==2.7
itypes==1.1.0
Jinja2==2.10
MarkupSafe==1.1.0
mysqlclient==1.3.13
numpy==1.15.1
oauthlib==2.1.0
openapi-codec==1.3.2
pandas==0.23.4
PyJWT==1.6.4
python-dateutil==2.7.3
python3-openid==3.1.0
pytz==2018.5
PyYAML==3.13
requests==2.20.0
requests-oauthlib==1.0.0
simplejson==3.16.0
six==1.11.0
social-auth-app-django==3.1.0
social-auth-core==2.0.0
uritemplate==3.0.0
urllib3==1.24.1
