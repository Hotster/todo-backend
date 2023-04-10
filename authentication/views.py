from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


@method_decorator(csrf_protect, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            'message': 'User created successfully',
            'user': UserSerializer(user).data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name='dispatch')
class UserLoginView(generics.GenericAPIView):

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        response_data = {
            'message': 'Login successful',
            'user': UserSerializer(user).data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response({'success': 'Logged out'})


@method_decorator(csrf_protect, name='dispatch')
class IsAuthenticatedView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        user = request.user

        if user.is_authenticated:
            response_data = {
                'authenticated': True,
                'message': 'User authenticated',
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'authenticated': False,
                'message': 'User is not authenticated',
                'user': None
            }
            return Response(response_data, status=status.HTTP_200_OK)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        return Response({'success': 'CSRF cookie set'})
