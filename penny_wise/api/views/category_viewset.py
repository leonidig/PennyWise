from rest_framework import viewsets
from ..models import Category
from ..serializers.category_serializer import CategorySerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from drf_spectacular.utils import extend_schema_view, extend_schema


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


@extend_schema_view(
    list=extend_schema(tags=['Category']),
    retrieve=extend_schema(tags=['Category']),
    create=extend_schema(tags=['Category']),
    update=extend_schema(tags=['Category']),
    partial_update=extend_schema(tags=['Category']),
    destroy=extend_schema(tags=['Category']),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
