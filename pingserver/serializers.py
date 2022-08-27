from xml.parsers.expat import model
from rest_framework.serializers import ModelSerializer

from .models import server


class serverListSerializer(ModelSerializer):
    class Meta:
        model = server
        fields = '__all__'
