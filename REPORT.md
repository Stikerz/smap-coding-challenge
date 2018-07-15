## Setup:

- Create virtualenv(Optional) using python 3.6
- Run pip install -r requirements.txt
- Run python manage.py makemigrations
- Run python manage.py migrate
- Run python manage.py runserver # Now go to localhost:8000

##Import

- Run python manage.py import 
  - Optional argument -u # specify consumer file location
   - Optional argument -c # specify consumption file location
   
   
## Testing
- Run python manage.py test consumption.tests #Run consumption test
