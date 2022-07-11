from django.urls import path, include
from rest_framework import routers
from mainapp.views import (
        UserView,
        ProfileView,
        ReferralProgramView,
        RefferalUrl
        )


router = routers.SimpleRouter()
router.register('user', UserView)
router.register('profile', ProfileView)
router.register('referral', ReferralProgramView)


urlpatterns =[
        path('get_referral_url/', RefferalUrl.as_view(), name='referral_url', ),
] + router.urls