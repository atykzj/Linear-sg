# LINEAR Backend
-----
## Changelog Notes
##### V1.0.1
Only using backend codes for this app, added docstrings and necessary information will be documented below. Removed Django Security Account creation login and password update.

##### V1.0.0
Rename `mlmodels` folder to `models`.

-----
## Run Commands

LINEAR working fullstack with django, react. All codes work locally only.
Calling prediction will save inference results to
```sh
C:\graph2plan-exploration\frontend\react_app\public\results
```

- Front End
```sh
(lr) C:\...\frontend\react_app>npm build
(lr) C:\...\frontend\react_app>npm start
```

Stores Django REST Framework API Calls for Google Cloud Deployment.
- To run backend Call.
```sh
(lr) C:\...\backend\django_app>python manage.py runserver
```

- Google cloud
Set up user authentication on google cloud platform and then at folder repo run the following command.
````sh
C:\...\backend\django_app>gcloud app deploy
````

-----

## File Structure
### Separate Files
#### 'app.yaml': Dockerfile 
Google cloud instance configuration, sets the commands to run this django app on Google cloud servers.

#### 'db.sqlite3':
Sql lite db for temporary storage of files for processing in the instance.
#### 'manage.py':
Django main app to run django api locally.
#### 'requirements.txt':
To download dependencies for Google cloud instance.

### 'mainapp' Folder
This folder consists of initialisation of the Django app, 'settings.py' consists of variables abstraction and settings.

### 'prediction' Folder
Folder contains the main API of the django app. 
1. 'apps.py' runs upon start up of code, loads the required model and data.
2. 'urls.py' sets up the browser entry point of the app to call via HTML.
3. 'views.py' is main content where all the code to run inference.
### 'users'
Outdated django app that was originally used for user authentication verification.

-----
## Selenium Image Scraping
Selenium scraping is a screenscraper that requires the use of a browser to automate the scraping of images by imitating human scrolling and clicking.
### Requirements
- Download selenium
- Download compatible chrome webdriver API from Google
- Download relevant python packages for image download from URL
- Set up a 'user.py' to load user credentials

### To run
Just follow the jupyter notebook, load the settings and configurations then run the code block.


-----
## Machine Learning Models and Process
1. Recommend style, images, material palette using cosine similarity.
10 Classes styles:
```['Contemporary', 'Eclectic', 'Industrial', 'Minimalistic', 'Modern', 'Retro', 'Scandinavian', 'Traditional', 'Transitional', 'Vintage']```
2. KNN - FAISS library for color palette generation of specified image.
