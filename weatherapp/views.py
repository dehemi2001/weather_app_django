from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
import requests
import datetime


def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        return render(request, 'weatherapp/index.html')

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}"
        PARAMS = {'units': 'metric'}

        # Get weather data
        weather_response = requests.get(url, params=PARAMS)
        data = weather_response.json()
        if weather_response.status_code != 200 or 'weather' not in data or 'main' not in data:
            raise ValueError("Weather API error")

        # Get image data
        query = city
        page = 1
        start = (page - 1) * 10 + 1
        searchType = 'image'
        city_url = f"https://www.googleapis.com/customsearch/v1?key={settings.GOOGLE_API_KEY}&cx={settings.GOOGLE_SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}"

        image_response = requests.get(city_url)
        image_data = image_response.json()
        print("Google API response:", image_data)
        search_items = image_data.get("items")
        if not search_items:
            image_url = None
        else:
            image_url = search_items[0]['link']

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except Exception as e:
        print("Exception:", e)
        messages.error(request, 'Entered data is not available to API')
        return render(request, 'weatherapp/index.html', {'exception_occurred': True})