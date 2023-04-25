from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, UserMessage


class MyCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {"first_name": "Name"}

    def __init__(self, *args, **kwargs):
        super(MyCreationForm, self).__init__(*args, **kwargs)

        for field_key, field_value in self.fields.items():
            field_value.widget.attrs.update({"class": "input"})


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name", "email", "username", "location", "short_intro", "bio", "profile_image",
            "social_github", "social_facebook", "social_twitter",
            "social_linkedin", "social_website"
        ]

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        for field_key, field_value in self.fields.items():
            field_value.widget.attrs.update({"class": "input"})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name", "description"
        ]

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for field_key, field_value in self.fields.items():
            field_value.widget.attrs.update({"class": "input"})


class MessageForm(ModelForm):
    class Meta:
        model = UserMessage
        fields = [
            "name", "email", "subject", "body"
        ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for field_key, field_value in self.fields.items():
            field_value.widget.attrs.update({"class": "input"})
