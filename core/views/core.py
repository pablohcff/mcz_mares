from django.shortcuts import render
import requests
from datetime import date

def extrair_dados(request):
    hoje = date.today()
    harbor = "al01"
    month = hoje.month
    days = f"[{hoje.day}]"

    url = f"https://tabuamare.devtu.qzz.io/api/v2/tabua-mare/{harbor}/{month}/{days}"
    response = requests.get(url)
    dados = response.json()
    
    return render(request, "core/index.html", 
    {"dados": dados})
