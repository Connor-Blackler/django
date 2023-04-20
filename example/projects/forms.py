from django.forms import ModelForm
from django import forms
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "demo_link",
                  "source_link", "tags", "featured_image"]
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for field_key, field_value in self.fields.items():
            field_value.widget.attrs.update({"class": "input"})
