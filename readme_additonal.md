
# Local and Heroku configuration

## Test it on local first found here

 `http://127.0.0.1:5000/`

# Heroku configuration

**Run this command.  Will likely need to run the collectstatic command before this one to have the latest css files:**

`heroku local`

* To shut down the local:

`sudo fuser -k 5000/tcp`

* **Note:** Will likely need to run "heroku login" in order to connect to Heroku.  Log in to Heroku before you do this.

**Connect to the remote repository:**

`heroku login`

heroku git:remote -a python-django-commerce

**Perhaps do this and make sure everything is committed to Git:**

`git add .`

**Commit the files**

`git commit -am "make it better"`

**Push the changes to the remote repository on Heroku:**

`git push heroku master`

**Note**: the branch could also be called "main" in Git.

* Whitenoise should be installed at the latest version.

* Also sometimes need to run collectstatic locally in the Python command line before pushing to Heroku:

    `python ./manage.py collectstatic`

To quit Ubuntu: `exit`


# Google Cloud Setup

* Install the CLI or SDK.

Create the remote repository with this.  This creates the rpository on Google Cloud which you can check with `git remote -v`.

`git remote add google https://source.developers.google.com/p/[PROJECT_NAME]/r/[REPO_NAME]`

Where:

* [PROJECT_NAME] is the name of your Google Cloud project.  This is `django-commerce-406118`.
* [REPO_NAME] is the name of your repository. This is `commerce`.

So run this command which I tested and it works:

`git remote add google https://source.developers.google.com/p/django-commerce-406118/r/commerce`


`git remote add google https://source.developers.google.com/p/django-commerce/r/commerce`


Create a repository:

`gcloud source repos create [REPO_NAME]`

`gcloud source repos create [commerce]`


Creating the remote repository:

`gcloud source repos create commerce`


C:\Users\geoff\OneDrive\Desktop\Git_Repositories\commerce>gcloud source repos create commerce
Created [commerce].
WARNING: You may be billed for this repository. See https://cloud.google.com/source-repositories/docs/pricing for details.

# ChatGPT instructions for Google Cloud

* [](https://chatgpt.com/share/63f267c4-a0d9-4342-b64b-a03dbe4607d0)

# General tips for deploying to Google Cloud

* [](https://medium.com/@muhammad-haseeb/how-to-deploy-a-django-project-on-google-cloud-for-free-a-step-by-step-tutorial-45d10fbb844d)

Run these commands in PS or Ubuntu:

`gcloud init`

`gcloud app deploy`

`gcloud app browse` to view the site.

This is the site: [https://django-commerce-406118.uk.r.appspot.com](https://django-commerce-406118.uk.r.appspot.com)
