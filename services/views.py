from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import Service
from .serializers import ServiceSerializer


# ============================================================
# SERVICE LIST / CREATE
# ============================================================

@extend_schema(
    request=ServiceSerializer,
    responses=ServiceSerializer,
    auth=[],
    tags=["Services"]
)
class ServiceListView(APIView):

    def get(self, request):

        services = Service.objects.all()

        serializer = ServiceSerializer(
            services,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = ServiceSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


# ============================================================
# SERVICE DETAIL
# ============================================================

@extend_schema(
    responses=ServiceSerializer,
    auth=[],
    tags=["Services"]
)
class ServiceDetailView(APIView):

    def get(self, request, id):

        try:

            service = Service.objects.get(
                id=id
            )

        except Service.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Service not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ServiceSerializer(
            service
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )