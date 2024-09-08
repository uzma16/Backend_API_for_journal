import jwt
from .models import User
from firebase_admin import auth
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from response import CustomJsonRender
from django.views.decorators.csrf import csrf_protect


# Create your views here.
class UserLogin(APIView):

    @staticmethod
    def post(request):
        id_token = request.data['id_token']
        fcm_token = request.data['fcm_token']
        user_timezone = request.data['timezone']
        user_timezone_name = request.data['timezone_name']
        decoded_token = auth.verify_id_token(id_token)
        phone = decoded_token['phone_number']
        user_exists = False
        user = User.objects.filter(phone=phone)

        if user:
            '''if user already exists'''
            user_exists = True
            user = User.objects.get(phone=phone)
            user.user_timezone = user_timezone
            user.user_timezone_name = user_timezone_name
            '''checking fcm token in db'''
            if user.fcm_token is None:
                user.fcm_token = []
                user.fcm_token.append(*fcm_token)
                user.save()
            else:
                '''if fcm token is new, add in the db'''
                if fcm_token[0] not in user.fcm_token:
                    user.fcm_token.append(*fcm_token)
                    user.save()
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)},status=status.HTTP_200_OK)
        else:
            '''creating new user and updating db'''
            User.objects.create(phone=phone)
            user = User.objects.get(phone=phone)
            user.fcm_token = fcm_token
            user.username = phone
            user.user_timezone = user_timezone
            user.user_timezone_name = user_timezone_name
            user.save()
            '''generating JWT token'''
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)},status=status.HTTP_200_OK)


class LoginWithSocialAuth(APIView):

    @staticmethod
    def post(request):
        id_token = request.data['id_token']
        fcm_token = request.data['fcm_token']
        user_timezone = request.data['timezone']
        user_timezone_name = request.data['timezone_name']
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        email = decoded_token['email']
        user_exists = False
        user = User.objects.filter(email=email)
        if user:
            '''if user already exists'''
            user_exists = True
            user = User.objects.get(email=email)
            user.user_timezone = user_timezone
            user.user_timezone_name = user_timezone_name
            '''checking fcm token in db'''
            if user.fcm_token is None:
                user.fcm_token = []
                user.fcm_token.append(*fcm_token)
                user.save()
            else:
                '''if fcm token is new, add in the db'''
                if fcm_token[0] not in user.fcm_token:
                    user.fcm_token.append(*fcm_token)
                    user.save()
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)},status=status.HTTP_200_OK)
        else:
            '''creating new user and updating db'''
            User.objects.create(email=email)
            user = User.objects.get(email=email)
            user.fcm_token = fcm_token
            user.username = email
            user.user_timezone = user_timezone
            user.user_timezone_name = user_timezone_name
            user.save()

            '''generating JWT token'''
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)},status=status.HTTP_200_OK)


class UserDetail(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    renderer_classes = (CustomJsonRender,)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False,  methods=['get'])
    def current_user(self, request):
        current_user = User.objects.get(username=self.request.user)
        serializer = ProfileSerializer(current_user)
        return Response(serializer.data)
