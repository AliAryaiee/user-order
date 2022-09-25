import jwt
from App.settings import SECRET_KEY
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import exceptions, permissions, status

from . import serializers


User = get_user_model()


class UserRegister(APIView):
    """
        User Register
    """

    def get_user_object(self, mobile: str):
        """
            Get User Object
        """
        try:
            return User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            return None

    def post(self, request):
        """
            Create New User by POST Request
        """
        serialized_user = serializers.UserRegisterSerializer(data=request.data)

        if serialized_user.is_valid(raise_exception=True):
            validated_data = serialized_user.validated_data
            # 0 - Check the Mobile Already Exists in the Database
            mobile = validated_data["mobile"]
            user_db = self.get_user_object(mobile)
            if user_db:
                return Response(
                    {"response": f"{mobile} Already Exists in Database!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 1 - Create User and Save It Into the Database
            del validated_data["confirm_password"]
            db_user = serialized_user.save()
            serialized_response = serializers.UserProfileSerializer(
                instance=db_user
            )

            # 2 - Return Token
            # _, token = AuthToken.objects.create(db_user)
            return Response({"user": serialized_response.data})


class UserProfile(APIView):
    """
        User Profile Endpoint
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_user_object(self, user_id: int):
        """
            Find User by UserID
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request):
        """
            Retrieve User Profile GET Request
        """
        JWT = request.headers["Authorization"].split(" ")[-1]
        if not JWT:
            raise exceptions.AuthenticationFailed("You Must Be Authenticated!")
        try:
            payload = jwt.decode(
                JWT,
                SECRET_KEY,
                algorithms=["HS256"]
            )
            db_user = self.get_user_object(user_id=int(payload["user_id"]))
            if db_user:
                serialized_data = serializers.UserProfileSerializer(
                    instance=db_user
                )
                return Response(serialized_data.data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                "The Token Has Benn Expired!"
            )
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid Token")
        return Response(
            {"response": "You Must Be Authenticated!"},
            status=status.HTTP_401_UNAUTHORIZED
        )
