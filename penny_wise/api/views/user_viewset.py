from rest_framework import viewsets
from ..models import User
from ..serializers.user_serializer import UserSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(tags=['User']),
    retrieve=extend_schema(tags=['User']),
    create=extend_schema(tags=['User']),
    update=extend_schema(tags=['User']),
    partial_update=extend_schema(tags=['User']),
    destroy=extend_schema(tags=['User']),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer