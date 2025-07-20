# from django.urls import path
# from .views import RegisterUser,LoginUser,UserSelfView

# urlpatterns = [
#     path('register/', RegisterUser.as_view(), name='register'),
#     path('login/', LoginUser.as_view(), name='login'), 
#     # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('me/', UserSelfView.as_view(), name='user-self'),
# ]


from django.urls import path
from .views import RegisterUser, LoginUser, UserSelfView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('me/', UserSelfView.as_view(), name='user-self'),
]
