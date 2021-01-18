# trip_ninja_auth_server

  `If you have installed this project in this machine before, make sure to clear old database.`

- Open a command line window and go to the project's directory.
  
  `pip install -r requirements.txt`

- Create the migrations for each app: 
  
  `python manage.py makemigrations`

- Run the migrations:

  `python manage.py migrate`

- initial data set:

  `python manage.py loaddata sampledata.yaml`
  
- Setup local environment variables. Create a file named '.env' in the root of the project with the following fields (Customized to your local postgres db name, user and password).
SECRET_KEY=''

`DB_NAME='trip_ninja_auth'
DB_USER='postgres'
DB_PASSWORD='password'

DB_HOST='localhost'
DB_PORT='5432'`

- Open another command line window.

  `workon theprojectname` or `source theprojectname/bin/activate` depending on if you are using virtualenvwrapper or just virtualenv.
- Go to the `backend` directory.

  `python manage.py runserver`
