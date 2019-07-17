from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action

from core.permission import IsCreatorOrReadOnly

from comments.models import Comment
from comments.serializers import CommentSerializer

from .serializers import PostSerializer, PostCommentSerializer
from .models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]

    def get_queryset(self):
        if self.action == 'comments':
            pk = self.kwargs.get('pk')
            return Comment.objects.filter(post_id=pk)

        if self.action == 'my':
            return Post.objects.filter(creator=self.request.user)

        return super().get_queryset()

    def get_serializer_class(self):
        # if self.action == 'retrieve':
        #     return PostCommentSerializer
        #
        # if self.action == 'comments':
        #     return CommentSerializer
        #
        # return super().get_serializer_class()
        default = super().get_serializer_class()
        return {
            'retrieve': PostCommentSerializer,
            'comments': CommentSerializer
        }.get(self.action, default)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


    @action(['GET'], True) #/<pk>/my => True /my => False
    def comments(self, request, pk):
        # queryset = self.get_queryset()
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        return self.list(request)

    @action(['GET'], False, permission_classes=[IsAuthenticated])
    def my(self, request):
        return self.list(request)
