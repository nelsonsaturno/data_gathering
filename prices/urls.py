from django.urls import path
from .api_views import NewPricesView


urlpatterns = [
    path('new-prices/', NewPricesView.as_view(), name='new_prices'),
]
