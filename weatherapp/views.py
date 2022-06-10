from django.shortcuts import render
import requests
from datetime import datetime
import geonamescache  # Used for match checking


def home(request):

    # Checks for legitimate cities
    if 'search-city' in request.POST:
        gc = geonamescache.GeonamesCache()
        while request.POST['search-city'] != '':
            cities = str(gc.get_cities_by_name(request.POST['search-city']))
            if request.POST['search-city'] in cities:
                city = request.POST['search-city']
                break
            elif request.POST['search-city'] not in cities:
                city = 'Amsterdam'
                break

        while request.POST['search-city'] == '':
            city = 'Amsterdam'
            break

    # Call current weather
    URL = 'https://api.openweathermap.org/data/2.5/weather'
    API_KEY = 'MY_KEY'
    PAR = {

        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    req = requests.get(url=URL, params=PAR)
    res = req.json()

    city = res['name']
    description = res['weather'][0]['description']
    temp = res['main']['temp']
    icon = res['weather'][0]['icon']
    country = res['sys']['country']
    day = datetime.now().strftime("%d/%m/%Y %H:%M")

    weather_data = {

        'description': description,
        'temp': temp,
        'icon': icon,
        'day': day,
        'country': country,
        'city': city
    }

    return render(request, 'weatherapp/home.html', weather_data)
