from django.urls import path
from .views import RegisterUser, LoginUser, UserSelfView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('login/', LoginUser.as_view(), name='login'),
    path('me/', UserSelfView.as_view(), name='user-self'),
]






































































