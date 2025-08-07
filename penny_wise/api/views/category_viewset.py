from rest_framework import viewsets
from ..models import Category
from ..serializers.category_serializer import CategorySerializer
from rest_framework.permissions import IsAuthenticated



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    swagger_schema_fields = {"tags": ["Category"]}

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     print(f">>> TRYING TO DELETE CATEGORY {instance.id}: {instance}")
    #     response = super().destroy(request, *args, **kwargs)
    #     exists = Category.objects.filter(id=instance.id).exists()
    #     print(f">>> EXISTS AFTER DELETE? {exists}")
    #     return response

