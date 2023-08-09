from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_panel.models import MainPageData
from admin_panel.serializers import PasswordChangeSerializer, MainPageDataSerializer
from admin_panel.utils import get_tokens_for_user
from mebleGudykaDjangoRESTapi import settings


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST.get('email')
        print('Email:', email)
        password = request.POST.get('password')
        print('password:', password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', 'username': user.username, 'localId': user.id,
                             'access_token_lifetime': settings.ACCESS_TOKEN_LIFETIME,
                             'refresh_token_lifetime': settings.REFRESH_TOKEN_LIFETIME, **auth_data},
                            status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'msg': 'The password has been changed'}, status=status.HTTP_200_OK)


class MainPageDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            data = MainPageData.objects.first()
            serializer = MainPageDataSerializer(data)
            return Response(serializer.data)
        except MainPageData.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            data = MainPageData.objects.first()
            serializer = MainPageDataSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MainPageData.DoesNotExist:
            serializer = MainPageDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

