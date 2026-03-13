from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Event, CustomUser
from .serializers import EventSerializer, GroupSerializer, UserSerializer


def assert_access(request):
    if request.user.is_superuser:
        return
    if request.user.groups.filter(name='Researcher').exists():
        return
    raise Exception("No access")


class EventDetail(APIView):
    """
    Retrieve, update or delete an event instance.
    """

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventList(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # assert_access(request)

        items = Event.objects.all()
        serializer = EventSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        # assert_access(request)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
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


class GroupList(APIView):
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


class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        print(f"User Login View .........................")
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
