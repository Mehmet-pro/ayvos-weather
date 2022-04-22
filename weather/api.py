import requests
import time
from .models import Cities,Logs
from django.contrib import messages
from django.http import Http404

def data(city):
    json_data={}
    url = "https://api.openweathermap.org/data/2.5/weather?appid=c923e3fe95c6eb4afc9b2fb4348a9b55&q="+city
    request = requests.get(url)
    if request:
        json_data = request.json() # weather data
    return json_data,request


def log(request,city):
    logs = Logs()
    error = False
    start = time.perf_counter()
    weather_data,response = data(city)
    logs.user_id = request.user
    logs.ip_address = request.META.get('REMOTE_ADDR')
    logs.resault = response.status_code
    try:
        logs.location_id = Cities.objects.get(city = city)
    except:
        logs.location_id = None
        error = True
    
    if weather_data:
        logs.response_state = True
    else:
        messages.success(request, response.status_code)
        logs.response_state = False
        error = True

    end = time.perf_counter()
    response_time = end-start
    logs.response_time = response_time * 1000
    logs.save()

    if error:
        raise Http404

    return weather_data