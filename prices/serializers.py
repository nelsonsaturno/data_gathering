from rest_framework import serializers


class NewPricesSerializer(serializers.Serializer):
    """
    Serializer to validate the data is in JSON format.
    """
    securities_data = serializers.JSONField(required=True)
