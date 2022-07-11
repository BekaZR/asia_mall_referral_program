from django.contrib import admin
from mainapp.models import (User,
                            Profile,
                            ReferralProgram)



admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ReferralProgram)



