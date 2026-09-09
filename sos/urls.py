from django.urls import path
from .views import TriggerSOSView

urlpatterns = [
    path('trigger/', TriggerSOSView.as_view(), name='trigger-sos'),
]