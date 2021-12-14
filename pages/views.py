from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StockData
from django.contrib import messages
from .forms import ContactForm
from django.urls import reverse_lazy

import requests
import json


APIKEY = '8FV7ILHNL2UNT059' 

DATABASE_ACCESS = True 
#if False, the app will always query the Alpha Vantage APIs regardless of whether the stock data for a given ticker is already in the local database

class HomePageView(TemplateView):
    template_name = "home.html"



@csrf_exempt
def get_stock_data(request):
    #get ticker from the AJAX POST request
    ticker = request.POST.get('ticker', 'null')
    ticker = ticker.upper()

    if DATABASE_ACCESS == True:
        #checking if the database already has data stored for this ticker before querying the Alpha Vantage API
        if StockData.objects.filter(symbol=ticker).exists(): 
            #We have the data in our database! Get the data from the database directly and send it back to the frontend AJAX call
            entry = StockData.objects.filter(symbol=ticker)[0]
            return HttpResponse(entry.data, content_type='application/json')

    #obtain stock data from Alpha Vantage APIs
    #get adjusted close data
    price_series = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={APIKEY}&outputsize=full').json()
    
    #get SMA (simple moving average) data
    sma_series = requests.get(f'https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval=daily&time_period=10&series_type=close&apikey={APIKEY}').json()

    #package up the data in an output dictionary 
    output_dictionary = {}
    output_dictionary['prices'] = price_series
    output_dictionary['sma'] = sma_series

    #save the dictionary to database
    temp = StockData(symbol=ticker, data=json.dumps(output_dictionary))
    temp.save()

    if(output_dictionary['prices']):
        messages.error(request, 'Não existem ativos com essa sigla')

    

    #return the data back to the frontend AJAX call 
    return HttpResponse(json.dumps(output_dictionary), content_type='application/json')

class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('pages:success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'pages/success.html'