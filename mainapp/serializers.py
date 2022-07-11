from rest_framework.response import Response
from rest_framework import (
        serializers,
        status
        )
from mainapp.models import (User,
                            Profile,
                            ReferralProgram)
from mainapp.servises import (
        create_token,
        check_token
    )
from datetime import datetime


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id", "user", "username", "about",
            "recomennded_by", "updated", "created", "recomennded_by"
            )
        
        read_only_fields = ("created", "updated", )
    
    def update(self, instance, validated_data):
        recomennded_by = validated_data.get('recomennded_by', None)
        if not recomennded_by is instance:
            try:
                instance.save()
                return instance
            except Exception as e:
                return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone_number", "password")
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        if not self.context:
            return user
        token = self.context.get('token')
        pk = check_token(token).get('token')
        user_referrals_profile = Profile.objects.filter(pk=pk).first()
        Profile.objects.filter(pk=user.pk).update(recomennded_by=user_referrals_profile)
        return user


class ReferralProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralProgram
        fields = ("id", "user", "token",)