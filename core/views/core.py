from django.shortcuts import render
import requests
from datetime import date, datetime

def extrair_dados(request):
    hoje = date.today()
    harbor_id = "al01"
    month = hoje.month
    days = f"[{hoje.day}]"

    url = f"https://tabuamare.devtu.qzz.io/api/v2/tabua-mare/{harbor_id}/{month}/{days}"
    response = requests.get(url)
    dados = response.json()

    agora = datetime.now().time()
    all_mares = []

    for harbor in dados.get("data", []):
        mean_level = harbor.get("mean_level", 1.0)
        for month_obj in harbor.get("months", []):
            for day in month_obj.get("days", []):
                for h in day.get("hours", []):
                    hora_obj = datetime.strptime(h["hour"], "%H:%M:%S").time()
                    level = h["level"]
                    tide_type = "preamar" if level >= mean_level else "baixa-mar"
                    all_mares.append({
                        "harbor": harbor["harbor_name"],
                        "weekday": day["weekday_name"],
                        "day": day["day"],
                        "month": month_obj["month_name"],
                        "hour": h["hour"],
                        "level": level,
                        "tide_type": tide_type,
                        "passed": hora_obj < agora,
                    })

    proximas = [m for m in all_mares if not m["passed"]]

    if proximas:
        mais_recente = proximas[0]
        seguinte = proximas[1:]
    else:
        mais_recente = all_mares[-1] if all_mares else None
        seguinte = []

    return render(request, "core/index.html", {
        "mais_recente": mais_recente,
        "seguinte": seguinte,
    })
