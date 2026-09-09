from django.urls import path
from .views import ProviderRegistrationView, TopProvidersListView

urlpatterns = [
    path('', TopProvidersListView.as_view(), name='top-providers'),
    path('register/', ProviderRegistrationView.as_view(), name='provider-register'),
]