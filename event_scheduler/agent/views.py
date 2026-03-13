from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt # Use this for simplicity in testing, but a proper CSRF token is needed for production.
from django.utils import timezone
from django.http import StreamingHttpResponse

from datetime import datetime
import requests
import json

from .agent1 import agent1_executor
from .agent2 import agent2_executor
from .agent3 import agent3_executor


def assert_access(request):
    if request.user.is_superuser:
        return
    if request.user.groups.filter(name='Researcher').exists():
        return
    raise Exception("No access")


def index(request):
    return HttpResponse("Hello, world! This is Agent app.")


def agent1(request):
    assert_access(request)
    context = {}
    return render(request, "home/agent1.html", context)


def agent2(request):
    assert_access(request)
    context = {}
    return render(request, "home/agent2.html", context)


def agent3(request):
    assert_access(request)
    context = {}
    return render(request, "home/agent3.html", context)


@csrf_exempt # Use this decorator or other CSRF handling methods
def agent1_handler(request):
    assert_access(request)
    # print('agent1_handler called')
    if request.method == 'POST':
        try:
            # Assuming you send JSON data
            data = json.loads(request.body)
            input = data.get('input')
            # print('input: ' + input)

            result = agent1_executor.invoke({"input": input})
            output = result['output']
            # print(result['output'])

            return JsonResponse({'status': 'success', 'message': output})
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt # Use this decorator or other CSRF handling methods
def agent2_handler(request):
    assert_access(request)
    # print('agent2_handler called')
    if request.method == 'POST':
        try:
            # Assuming you send JSON data
            data = json.loads(request.body)
            input = data.get('input')
            # print('input: ' + input)

            output = agent2_executor.invoke({"input": input})
            # output = result['output']

            return JsonResponse({'status': 'success', 'message': output})
        except Exception as e:
            print(f"exception 1.")
            return HttpResponseBadRequest(f'Error: {e}')
    print(f"error 2.")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt # Use this decorator or other CSRF handling methods
def agent3_handler(request):
    assert_access(request)
    # print('agent3_handler called')
    if request.method == 'POST':
        try:
            # Assuming you send JSON data
            data = json.loads(request.body)
            input = data.get('input')
            print('input: ' + input)

            response = agent3_executor() #.invoke({"input": input})
            # output = result['output']
            # print(result['output'])
            print(f'got output ...')

            # return JsonResponse({'status': 'success', 'message': output})
            # return StreamingHttpResponse(output)
            return response
        except Exception as e:
            print(f"exception 1.")
            return HttpResponseBadRequest(f'Error: {e}')
    print(f"error 2.")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
