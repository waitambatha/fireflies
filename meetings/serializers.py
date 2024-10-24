from rest_framework import serializers
from .models import Transcript
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data
class TranscriptSummarySerializer(serializers.Serializer):
    transcriptId = serializers.CharField(required=True)


class UploadAudioSerializer(serializers.Serializer):
    webhook = serializers.URLField(required=True)
    audio_url = serializers.URLField(required=True)
    title = serializers.CharField(max_length=255, required=True)
    attendees = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            required=False
        ),
        required=False,
        allow_empty=True
    )







