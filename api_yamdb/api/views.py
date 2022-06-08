from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Review, Title
from .paginations import UserPagination
from .permissions import HasAdminRole, HasModeratorRole, IsOwner
from .serializers import (SignUpSerializer, UserSerializer,
                          MyTokenObtainPairSerializer, UserSelfSerializer,
                          CommentSerializer, ReviewSerializer)

User = get_user_model()


class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request):
        if not User.objects.filter(**request.data).exists():
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(**request.data)
        confirmation_code = get_random_string(length=32)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Код подтверждения для YAMDB',
            message=confirmation_code,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.data.get('email')]
        )

        return Response(request.data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class UserSelfView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSelfSerializer(user)

        return Response(serializer.data)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        print(user.role, request.data.get('role'))
        serializer = UserSelfSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    pagination_class = UserPagination
    serializer_class = UserSerializer
    permission_classes = (HasAdminRole,)
    lookup_field = 'username'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwner, HasAdminRole, HasModeratorRole)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwner, HasAdminRole, HasModeratorRole)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
