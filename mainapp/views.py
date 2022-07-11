from datetime import date

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from django.http import JsonResponse

from mainapp.permissions import DontCreate
from mainapp.servises import get_register_url_for_refferal

from mainapp.models import (
        User,
        Profile,
        ReferralProgram
        )
from mainapp.serializers import (
        UserSerializer,
        ProfileSerializer,
        ReferralProgramSerializer,
        )


User = get_user_model()


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DontCreate]
    
    @action(methods=['post'], detail=False, serializer_class=UserSerializer, permission_classes = [AllowAny])
    def reqister(self, request):
        if request.method == "POST":
            token = request.query_params.get('token', None)
            if not token:
                serializer = UserSerializer(data=request.POST)
            else:
                serializer = UserSerializer(data=request.POST,
                                        context={"token": token})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ReferralProgramView(viewsets.ModelViewSet):
    queryset = ReferralProgram.objects.all()
    serializer_class = ReferralProgramSerializer


class RefferalUrl(generics.RetrieveUpdateAPIView):
    def get(self, request):
        
        user_profile_pk = request.user.users_profile.pk
        
        user_referral = ReferralProgram.objects.filter(pk=user_profile_pk).first()
        
        referral_url = get_register_url_for_refferal(request=request, token=user_referral.token)
        
        return JsonResponse({"url": referral_url})