
# Some of the commands necessary to set it up:

**Test it on local first found here:**

 http://127.0.0.1:5000/

**Run this command:**

heroku local

**To shut down the local:**

sudo fuser -k 5000/tcp

* Will likely need to run "heroku login" in order to connect to Heroku.

**Connect to the remote repository:**

heroku git:remote -a python-django-commerce


**Push the changes to the remote repository on Heroku:**

git push heroku master

Note: the branch could also be called "main" in Git.

**Can also use this command on Linux Ubuntu:**

git push heroku master

* Whitenoise should be installed at the latest version.

**Also sometimes need to run collectstatic locally:**

python ./manage.py collectstatic
