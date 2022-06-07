from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import USER_ROLE_CHOICES

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        confirmation_code = get_random_string(length=32)
        if validated_data['username'] == 'me':
            error = {'username': ['Нельзя создать пользователя с username me']}
            raise exceptions.ValidationError(error)
        user = User.objects.create_user(
            confirmation_code=confirmation_code, **validated_data)
        send_mail(
            subject='Код подтверждения для YAMDB',
            message=confirmation_code,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[validated_data.get('email')]
        )
        user.save()
        return user


class MyTokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = None

    default_error_messages = {
        "no_active_account": _(
            "Активная учетная запись с указанными учетными данными не найдена")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.NotFound(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('username', 'email', 'role')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, default='user')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            error = {'username': ['Нельзя создать пользователя с username me']}
            raise exceptions.ValidationError(error)
        return super().create(validated_data)
