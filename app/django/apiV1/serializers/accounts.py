from django.db import transaction
from rest_framework import serializers

from accounts.models import User, StaffAuth, Profile, Todo


# Accounts --------------------------------------------------------------------------
class StaffAuthInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAuth
        fields = ('pk', 'user', 'company', 'is_staff', 'is_project_staff',
                  'allowed_projects', 'assigned_project', 'contract', 'payment',
                  'notice', 'project_cash', 'project_docs', 'project', 'company_cash',
                  'company_docs', 'human_resource', 'company_settings', 'auth_manage')

    @transaction.atomic
    def create(self, validated_data):
        # 1. 권한정보 테이블 입력
        many_to_many = {'allowed_projects': validated_data.pop('allowed_projects')}
        instance = StaffAuth.objects.create(**validated_data)

        # Save many-to-many relationships after the instance is created.
        for field_name, value in many_to_many.items():
            field = getattr(instance, field_name)
            field.set(value)

        # 2. 프로필 정보가 있는지 확인 후 없으면 기본 프로필 생성
        try:
            Profile.objects.get(user=validated_data['user'])
        except Profile.DoesNotExist:
            empty_profile = Profile(user=instance.user)
            empty_profile.save()

        return instance


class ProfileInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pk', 'name', 'birth_date', 'cell_phone')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='변경할 필요가 없으면 비워 두십시오.',
        style={'input_type': 'password', 'placeholder': '비밀번호'}
    )
    staffauth = StaffAuthInUserSerializer(read_only=True)
    profile = ProfileInUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'username', 'is_active', 'is_superuser',
                  'date_joined', 'password', 'staffauth', 'profile')

    def save(self):
        instance = User(email=self.validated_data['email'],
                        username=self.validated_data['username'])
        password = self.validated_data['password']
        instance.set_password(password)
        instance.save()
        self.instance = instance
        return self.instance


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_empty_file=False, required=False)

    class Meta:
        model = Profile
        fields = ('pk', 'user', 'name', 'birth_date',
                  'cell_phone', 'image', 'like_posts', 'like_comments')


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('pk', 'user', 'title', 'completed', 'soft_deleted')
