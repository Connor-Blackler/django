from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from .helpers import search_projects, paginate_projects


def projects(request):
    my_projects, search = search_projects(request)
    custom_range, my_projects = paginate_projects(request, my_projects, 3)

    context = {"projects": my_projects, "filter": search,
               "custom_range": custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-projects.html', {"project": projectObj})


@ login_required(login_url="login")
def create_project(request):
    my_form = ProjectForm()
    my_profile = request.user.profile

    if request.method == "POST":
        my_form = ProjectForm(request.POST, request.FILES)
        if my_form.is_valid():
            new_project = my_form.save(commit=False)
            new_project.owner = my_profile
            new_project.save()
            return redirect("my-profile")

    context = {"form": my_form}
    return render(request, "projects/project_form.html", context)


@ login_required(login_url="login")
def update_project(request, pk):
    my_profile = request.user.profile
    my_project = my_profile.project_set.get(id=pk)

    my_form = ProjectForm(instance=my_project)

    if request.method == "POST":
        my_form = ProjectForm(request.POST, request.FILES, instance=my_project)
        if my_form.is_valid():
            my_form.save()
            return redirect("my-profile")

    context = {"form": my_form}
    return render(request, "projects/project_form.html", context)


@ login_required(login_url="login")
def delete_project(request, pk):
    my_profile = request.user.profile
    my_project = my_profile.project_set.get(id=pk)

    if request.method == "POST":
        my_project.delete()
        return redirect("projects")

    context = {"object": my_project}
    return render(request, "delete_template.html", context)
