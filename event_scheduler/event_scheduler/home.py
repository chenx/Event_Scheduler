from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    can_access_api = request.user.groups.filter(name='researcher').exists() or request.user.is_superuser

    context = {'can_access_api': can_access_api}
    return render(request, "home/index.html", context)
