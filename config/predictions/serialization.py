from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):
    url = serializers.URLField()