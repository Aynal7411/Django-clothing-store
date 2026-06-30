from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    CustomTokenObtainPairView,
    LogoutView,
)
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


from django.urls import path
from .api_views import register_view, login_view, profile_view,logout_view

urlpatterns = [

    path(
        "register/",
        register_view,
        name="register",
    ),
    path(
    "login/",
    login_view,
    name="login",
),
path(
    "profile/",
    profile_view,
    name="profile",
),
path(
    "logout/",
    logout_view,
    name="logout",
),

]
