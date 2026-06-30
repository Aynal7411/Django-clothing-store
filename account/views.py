
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    MyTokenObtainPairSerializer,ProfileSerializer
)


class RegisterView(APIView):
    """
    Register a new user
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "User registered successfully."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Login API (JWT)
    """
    serializer_class = MyTokenObtainPairSerializer


class ProfileView(APIView):
    """
    Logged in user's profile
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(
            {
                "id": request.user.id,
                "name": request.user.name,
                "mobile": request.user.mobile,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    Logout API
    Blacklists the refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "success": True,
                    "message": "Logout successful."
                },
                status=status.HTTP_205_RESET_CONTENT,
            )

        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
