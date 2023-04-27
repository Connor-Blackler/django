from django.forms import ModelForm
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "demo_link",
                  "source_link", "featured_image"]
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for field_key, field_value in self.fields.items():
            field_value.widget.attrs.update({"class": "input"})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]

        labels = {
            "value": "Place your vote",
            "body": "Additionally add a comment"
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for field_key, field_value in self.fields.items():
            field_value.widget.attrs.update({"class": "input"})
