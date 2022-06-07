from django.urls import path, include
from rest_framework import routers

from api.views import (MyTokenObtainPairView, SignUpAPIView, UserViewSet,
                       UserSelfView)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, 'user')

urlpatterns = [
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(), name='login'),
    path('v1/users/me/', UserSelfView.as_view(), name='user_self'),
    path('v1/', include(router_v1.urls)),
]
