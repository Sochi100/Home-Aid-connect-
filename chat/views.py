from django.db.models import Q
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Message
from .serializers import MessageSerializer


@extend_schema(tags=["Chat / Messages"])
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        recipient_id = self.request.query_params.get('recipient_id')

        if recipient_id:
            return Message.objects.filter(
                (Q(sender=user) & Q(recipient_id=recipient_id)) |
                (Q(sender_id=recipient_id) & Q(recipient=user))
            )

        return Message.objects.filter(Q(sender=user) | Q(recipient=user))