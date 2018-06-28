from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .serializers import NewPricesSerializer
from .models import SecurityPrice, Security
from websocket import create_connection
import json


class NewPricesView(APIView):
    """
    Create a new price for each security in the Database
    """
    permission_classes = (AllowAny,)
    serializer_class = NewPricesSerializer

    def manage_securities_data(self, data, registered):
        """
        Check the data received has one entry for each Security registered.
        Params:
            data: JSON data received
            registered: DateTime to register each price
        """
        if len(data.keys()) != Security.objects.all().count():
            return ParseError(detail="There aren't all the securities registered.")
        new_prices = []
        for key, value in data.items():
            try:
                security = Security.objects.get(name=key)
                new_prices += [SecurityPrice(
                    security=security, price=float(value), registered=registered
                )]
            except ObjectDoesNotExist:
                return ParseError(detail="There is a security not registered.")
        for np in new_prices:
            np.save()

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        registered = datetime.now().replace(tzinfo=None)
        self.manage_securities_data(json.loads(request.data['securities_data']), registered)
        # Create Websocket connection
        ws = create_connection("ws://127.0.0.1:8000/ws/prices/")  # URL to the Data Processing Tool
        ws.send(str(registered))
        ws.close()
        return Response(status=204)
