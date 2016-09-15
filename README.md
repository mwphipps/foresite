# foresite
Django Project for Weather &amp; Surf Conditions

App for showing local weather and surfing conditions.
Note: Before building this project, you will need to supply your own OpenWeatherMap & Magic Seaweed API keys. Look in foresite/conditions/views.py for "". It will be in 3 places in the file. 1 for OWM and one for MS.
To get your own API key for each of these, visit http://openweathermap.org/appid &http://magicseaweed.com/developer/api.

You should create a new virtualenv and activate it before installing.

Install: pip install -r requirements.txt
To use: Administration credentials are: admin/password
cd ~/django-forecast/foresite
python manage.py runserver_plus 127.0.0.1:8000
