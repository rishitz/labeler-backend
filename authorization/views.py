from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authorization.serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token_key = request.headers.get("Authorization", "").split("Token ")[-1]
        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(
                {"detail": "Invalid token or user is not logged in"},
                status=status.HTTP_400_BAD_REQUEST,
            )
