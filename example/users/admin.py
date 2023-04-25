from django.contrib import admin
from .models import Profile, Skill, UserMessage

# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(UserMessage)
