from django.urls import path, include
from rest_framework import routers

from api.views import (MyTokenObtainPairView, SignUpAPIView, UserViewSet,
                       UserSelfView, CommentViewSet, ReviewViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, 'user')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(), name='login'),
    path('v1/users/me/', UserSelfView.as_view(), name='user_self'),
    path('v1/', include(router_v1.urls)),
]
