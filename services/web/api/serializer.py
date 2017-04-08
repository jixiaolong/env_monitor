from django.contrib.auth.models import User
from rest_framework import serializers
from db.models import BaseInfo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class BaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseInfo
        fields = ('id', 'base_num', 'sim_number', 'sim_price', 'sim_type_info',
                  'monitor_place', 'longitude', 'latitude', 'create_time',
                  'modified_time', 'current_status')
