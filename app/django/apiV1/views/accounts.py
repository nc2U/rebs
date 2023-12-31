from allauth.account.forms import default_token_generator
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permission import *
from ..pagination import *
from ..serializers.accounts import *

from accounts.models import User, StaffAuth, Profile, Todo


# Accounts --------------------------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPaginationThreeThousand
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class StaffAuthViewSet(viewsets.ModelViewSet):
    queryset = StaffAuth.objects.all()
    serializer_class = StaffAuthInUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsStaffOrReadOnly)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScrapeViewSet(viewsets.ModelViewSet):
    queryset = Scrape.objects.all()
    serializer_class = ScrapeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)
    filterset_fields = ('user',)
    search_fields = ('title', 'post__title', 'post__content')


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = PageNumberPaginationFifty
    permission_classes = (permissions.IsAuthenticated, IsOwnerOnly)
    filterset_fields = ('user', 'soft_deleted')
    search_fields = ('title',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CheckPasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        password = request.data.get('password', None)

        if not password:
            return Response({'detail': 'Password not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=request.data.get('email'), password=password)

        if user is not None:
            # Password is correct
            return Response({'detail': 'Password correct.'}, status=status.HTTP_200_OK)
        else:
            # Password is correct
            return Response({'detail': 'Password incorrect.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the old password is correct
            old_password = serializer.validated_data.get('old_password')
            if not check_password(old_password, request.user.password):
                return Response({'detail': '패스워드를 맞지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the password
            new_password = serializer.validated_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()

            # Update the user's session to prevent the user from being logged out
            update_session_auth_hash(request, request.user)

            return Response({'detail': '패스워드가 변경되었습니다.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Find the user with the given email
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': '입력한 이메일이 등록된 이메일과 같지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a password reset token
            token = default_token_generator.make_token(user)

            # Create a password reset link
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f'{request.get_host()}/#/accounts/pass-reset?uidb64={uidb64}&token={token}'

            # Send the password reset email
            subject = f'[Rebs] {user.username}님 계정 비밀번호 초기화 링크 안내드립니다.'
            message = f'비밀번호를 재설정 하기 위해서 다음 링크를 클릭 하세요.: {reset_link}'
            send_mail(subject, message, 'info@brdnc.co.kr', [email])

            return Response({'detail': '비밀번호 재설정을 위한 이메일을 발송했습니다.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
