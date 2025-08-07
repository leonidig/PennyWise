from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView

@extend_schema(
    tags=['CSRF'],
    responses={200: OpenApiResponse(description='CSRF cookie set')}
)
class Csrf(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'detail': 'CSRF cookie set'})