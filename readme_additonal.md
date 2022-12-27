
# Some of the commands necessary to set it up:

**Test it on local first found here:**

 http://127.0.0.1:5000/

gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ heroku local

**To shut down the local:**

gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ sudo fuser -k 5000/tcp
[sudo] password for gfarnell:

**Connect to the remote repository:**

gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ heroku git:remote -a python-django-commerce

set git remote heroku to https://git.heroku.com/python-django-commerce.git

**Push the changes to the remote repository on Heroku:**

gfarnell@HP_laptop:/mnt/c/Users/geoff/OneDrive/Desktop/Git_Repositories/commerce$ heroku push master

Note: the branch could also be called "main" in Git.

**Cn also use this command on Linux Ubuntu:**

git push heroku master