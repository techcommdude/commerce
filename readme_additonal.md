
Some of the commands necessary to set it up:

gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ heroku local


gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ sudo fuser -k 5000/tcp
[sudo] password for gfarnell:



gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ heroku git:remote -a python-django-commerce

set git remote heroku to https://git.heroku.com/python-django-commerce.git


gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ heroku push master