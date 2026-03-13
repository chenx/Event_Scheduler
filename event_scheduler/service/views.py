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

from datetime import datetime
import requests
import json

from .models import DataStore
from .serializers import DatastoreSerializer


# END_POINT_EVENTS = "https://renaldo-undemonstrational-gullably.ngrok-free.dev/api/events/"
END_POINT_EVENTS = "http://127.0.0.1:8000/api/events/"


def index(request):
    return HttpResponse("Hello, world! This is Service app.")


def test(request):
    response = requests.get(END_POINT_EVENTS)
    # print(f"response.status_code = {response.status_code}", response.json())

    if response.status_code == 200:
        data = response.json()
        context = {}
        return render(request, "home/test.html", context)
    return None


def datastore(request):
    data_store = DataStore.objects.all()
    print(f"DataStore all_items: {data_store}")
    for item in data_store:
        print(item.id)

    context = {"datastore": data_store}
    return render(request, "home/datastore.html", context)


# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def events(request):
    response = requests.get(END_POINT_EVENTS)
    # print(f"response.status_code = {response.status_code}", response.json())

    data_store_uids = DataStore.objects.values_list('uid', flat=True)
    # print(f"DataStore all_items: {data_store_uids}")

    if response.status_code == 200:
        data = response.json()
        context = {"events": data, "data_store_uids": data_store_uids}
        # print(data)
        return render(request, "home/events.html", context)
    return None


def events_for_owner(request, owner_id):
    response = requests.get(END_POINT_EVENTS)
    # print(f"response.status_code = {response.status_code}", response.json())
    data_store_uids = DataStore.objects.values_list('uid', flat=True)

    if response.status_code == 200:
        data = response.json()
        data = [item for item in data if item['owner'] == owner_id]
        owner_name = data[0]["owner_name"] if len(data) > 0 else ""
        context = {"events": data, "owner_name": owner_name, "data_store_uids": data_store_uids}
        # print(context)
        return render(request, "home/events.html", context)
    return None


def event(request, event_id):
    # api_key = "YOUR_API_KEY"
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    url = f"{END_POINT_EVENTS}{event_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        format_string = "%Y-%m-%dT%H:%M:%SZ"
        startTime = datetime.strptime(data["start_time"], format_string)
        endTime = datetime.strptime(data["end_time"], format_string)
        createTime = datetime.strptime(data["created_at"], format_string)
        lastUpdateTime = datetime.strptime(data["last_updated"], format_string)

        context = {
            "event_id": data["event_id"],
            "title": data["title"],
            "description": data["description"],
            "start_time": startTime.strftime("%Y-%m-%d %H:%M"),
            "end_time": endTime.strftime("%H:%M"),
            "owner": data["owner"],
            "created_at": createTime,
            "last_updated": lastUpdateTime,
            # "temperature": data["main"]["temp"],
            # "description": data["weather"][0]["description"]
        }
        return render(request, "home/event.html", context)
    return None


@csrf_exempt # Use this decorator or other CSRF handling methods
def save_data_view(request):
    if request.method == 'POST':
        try:
            # Assuming you send JSON data
            data = json.loads(request.body)
            uid = data.get('event_id')
            owner = data.get('owner')
            title = data.get('title')

            # Save to database
            DataStore.objects.create(uid=uid, title=title, description=owner, created_at=timezone.now())

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@csrf_exempt # Use this decorator or other CSRF handling methods
def delete_data_view(request):
    if request.method == 'POST':
        try:
            # Assuming you send JSON data
            data = json.loads(request.body)
            uid = data.get('event_id')

            # Delete from database
            DataStore.objects.filter(uid=uid).delete()

            return JsonResponse({'status': 'success', 'message': 'Data deleted successfully'})
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt # Use this decorator or other CSRF handling methods
def save_datastore_view(request):
    if request.method == 'POST':
        try:
            # Assuming you send JSON data
            data = json.loads(request.body)
            uid = data.get('uid')
            title = data.get('title')
            description = data.get('description')

            # Save to database
            DataStore.objects.create(uid=uid, title=title, description=description, created_at=timezone.now())

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@csrf_exempt # Use this decorator or other CSRF handling methods
def delete_datastore_view(request):
    if request.method == 'POST':
        try:
            # Assuming you send JSON data
            data = json.loads(request.body)
            id = data.get('id')

            # Delete from database
            DataStore.objects.filter(id=id).delete()

            return JsonResponse({'status': 'success', 'message': 'Data deleted successfully'})
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt # Use this decorator or other CSRF handling methods
def delete_all_datastore_view(request):
    if request.method == 'POST':
        try:
            # Delete all rows from database
            DataStore.objects.all().delete()

            return JsonResponse({'status': 'success', 'message': 'All data deleted successfully'})
        except Exception as e:
            return HttpResponseBadRequest(f'Error: {e}')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


class DatastoreList(APIView):
    """
    API endpoint for read/write
    """

    def get(self, request):
        items = DataStore.objects.all()
        serializer = DatastoreSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DatastoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
