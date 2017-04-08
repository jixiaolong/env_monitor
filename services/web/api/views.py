from rest_framework import viewsets
from django.contrib.auth.models import User
from serializer import UserSerializer, BaseInfoSerializer
from db.models import BaseInfo


class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class BaseInfoViewSet(viewsets.ModelViewSet):
    queryset = BaseInfo.objects.all().order_by('id')
    serializer_class = BaseInfoSerializer
