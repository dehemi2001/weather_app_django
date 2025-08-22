from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
import requests
import datetime


def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        # On a GET request, render the template without any data.
        return render(request, 'weatherapp/index.html')

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}"
        PARAMS = {'units': 'metric'}

        query = city
        page = 1
        start = (page - 1) * 10 + 1
        searchType = 'image'
        city_url = f"https://www.googleapis.com/customsearch/v1?key={settings.GOOGLE_API_KEY}&cx={settings.GOOGLE_SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}"

        image_data = requests.get(city_url).json()
        search_items = image_data.get("items")
        image_url = search_items[0]['link']

        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {'description': description, 'icon': icon, 'temp': temp, 'day': day, 'city': city, 'exception_occurred': False, 'image_url': image_url})

    except (KeyError, IndexError, TypeError, requests.exceptions.RequestException):
        messages.error(request, 'Entered data is not available to API')
        return render(request, 'weatherapp/index.html', {'exception_occurred': True})