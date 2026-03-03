from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, CustomUser
from .serializers import EventSerializer, GroupSerializer, UserSerializer


def assert_access(request):
    if request.user.is_superuser:
        return
    if request.user.groups.filter(name='researcher').exists():
        return
    raise Exception("No access")


class EventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assert_access(request)

        items = Event.objects.all()
        serializer = EventSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        assert_access(request)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assert_access(request)

        items = CustomUser.objects.all().filter(is_superuser=False)
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        assert_access(request)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assert_access(request)

        items = Group.objects.all().filter()
        serializer = GroupSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        assert_access(request)

        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
