from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.permission import IsCreatorOrReadOnly

from .serializers import CommentSerializer
from .models import Comment


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]
    filterset_fields = ['post_id']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
