from rest_framework import serializers

from .models import Client, Reseller, User

class ResellerSerializer(serializers.HyperlinkedModelSerializer):
    usage = serializers.SerializerMethodField('get_usage')

    class Meta:
        model = Reseller
        fields = ('instance_id', 'usage', 'limit', 'token')

    def get_usage(self, obj):
        return obj.get_usage()
