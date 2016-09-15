import pyowm
import requests

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.views.generic.edit import ProcessFormView

from django.views import generic

from django.views.generic import View

from django import forms

from datetime import datetime

# Using this https://github.com/csparpa/pyowm python wrapper for openweathermap.org API
# to get weather condition and air temperature based on city name

owm = pyowm.OWM('YOUR_OWM_API_KEY')

### OCEANICIC DATA ###

# Using the Magic Seaweed API (currently in beta) http://magicseaweed.com/developer/api
# to get wave heights. water temperature, and tides from a spot near Bogue, NC.

# Cache provider to be used
from pyowm.caches.lrucache import LRUCache
cache = LRUCache()

# The index view is only loaded once
class IndexView(View):
    def get(self, request, *args, **kwargs):

        observation = owm.weather_at_place('Bogue,us')

        w = observation.get_weather()
        w_loc = observation.get_location()
        w_loc_name = w_loc.get_name()
        w_timestamp = observation.get_reception_time()
        w_time = datetime.fromtimestamp(int(w_timestamp)).strftime("%A, %d. %B %Y %I:%M%p")
        w_status = w.get_status()
        w_ftemp = int(round(w.get_temperature('fahrenheit')['temp']))

        ymd = datetime.fromtimestamp(int(w_timestamp)).strftime("%Y%m%d")
        begin_date = ymd
        end_date = ymd

        mswApiOnline = True
        nightTime = False

        #Oceanic Information location defined by Magic Seaweed "spot" ID below
        msw_api_response = requests.get("http://magicseaweed.com/api/YOUR_MSW_API_KEY/forecast/?spot_id=3664")

        if msw_api_response.status_code == 200:
        	msw_api_object = msw_api_response.json()

        if msw_api_response.status_code != 200:
        	mswApiOnline = False

        cur_wave_height = msw_api_object[0]["swell"]["components"]["combined"]["height"]
        cur_wave_period = msw_api_object[0]["swell"]["components"]["combined"]["period"]

        tom_wave_height = msw_api_object[10]["swell"]["components"]["combined"]["height"]
        tom_wave_period = msw_api_object[10]["swell"]["components"]["combined"]["period"]

        third_wave_height = msw_api_object[18]["swell"]["components"]["combined"]["height"]
        third_wave_period = msw_api_object[18]["swell"]["components"]["combined"]["height"]

        # Test data output
	    #print tom_wave_height

        return render(request, 'conditions/index.html', {
            'title': "Weather & Tides",
            'weather_observation' : w,
            'weather_status' : w_status,
            'weather_temp' : w_ftemp,
            'weather_time' : w_time,
            'weather_location' : w_loc_name,
            'current_wave_height' : cur_wave_height,
			'current_wave_duration' : cur_wave_period,
			'tomorrow_wave_height' : tom_wave_height,
			'tomorrow_wave_duration' : tom_wave_period,
			'day_after_tomorrow_wave_height' : third_wave_height,
			'day_after_tomorrow_wave_duration' : third_wave_period,
        })
