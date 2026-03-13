from django.http import HttpResponse
from django.shortcuts import render

import requests

def index(request):
    can_access_api = request.user.groups.filter(name='Researcher').exists() or request.user.is_superuser

    # s = requests.Session()
    # print(f"session: {s.auth}")

    context = {'can_access_api': can_access_api}
    return render(request, "home/index.html", context)
