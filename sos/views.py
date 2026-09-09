from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import EmergencyAlert
from .serializers import EmergencyAlertSerializer


@extend_schema(tags=["Emergency SOS"])
class TriggerSOSView(generics.CreateAPIView):
    serializer_class = EmergencyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "success": True,
                "message": "EMERGENCY ALERT SENT. Help and responders have been notified.",
                "alert": serializer.data
            },
            status=status.HTTP_201_CREATED
        )