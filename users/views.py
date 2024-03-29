from django.contrib.auth import authenticate

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User
from .serializers import UserSerializer, LoginSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        return {
            'login': AuthTokenSerializer,
        }.get(self.action, super().get_serializer_class())

    @action(['POST'], False, permission_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        # serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # user = authenticate(**serializer.data)
        # if user is None:
        #     raise AuthenticationFailed()
        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })
