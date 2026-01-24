import shutil
from commerce.wsgi import application


# Copy the SQLite database to /tmp
shutil.copy2('db.sqlite3', '/tmp/db.sqlite3')

app = application