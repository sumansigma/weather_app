import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.http import HttpResponse

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=584fc5b2c62361d9c469e1a26a59914c'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        print(r)
        try:

            city_weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }
            print(city_weather)
            weather_data.insert(0,city_weather)

        except Exception as e:
              HttpResponse(e)

            

       

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)
