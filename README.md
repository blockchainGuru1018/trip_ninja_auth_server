# trip_ninja_auth_server

  `If you have installed this project in this machine before, make sure to clear old database.`

- Open a command line window and go to the project's directory.
  
  `pip install -r requirements.txt`

- Create the migrations for each app: 
  
  `python manage.py makemigrations`

- Run the migrations:

  `python manage.py migrate`
- Open another command line window.

  `workon theprojectname` or `source theprojectname/bin/activate` depending on if you are using virtualenvwrapper or just virtualenv.
- Go to the `backend` directory.

  `python manage.py runserver`
