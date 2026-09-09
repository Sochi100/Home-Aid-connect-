from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import ProviderProfile
from .serializers import ProviderProfileSerializer


@extend_schema(tags=["Providers / Artisans"])
class ProviderRegistrationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProviderProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        request.user.role = 'ARTISAN'
        request.user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Providers / Artisans"])
class TopProvidersListView(generics.ListAPIView):
    queryset = ProviderProfile.objects.all().order_by('-rating')
    serializer_class = ProviderProfileSerializer
    permission_classes = [permissions.AllowAny]