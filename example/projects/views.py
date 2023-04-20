from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-projects.html', {"project": projectObj})


def create_project(request):
    my_form = ProjectForm()

    if request.method == "POST":
        my_form = ProjectForm(request.POST)
        if my_form.is_valid():
            my_form.save()
            return redirect("projects")

    context = {"form": my_form}
    return render(request, "projects/project_form.html", context)


def update_project(request, pk):
    my_project = Project.objects.get(id=pk)
    my_form = ProjectForm(instance=my_project)

    if request.method == "POST":
        my_form = ProjectForm(request.POST, instance=my_project)
        if my_form.is_valid():
            my_form.save()
            return redirect("projects")

    context = {"form": my_form}
    return render(request, "projects/project_form.html", context)


def delete_project(request, pk):
    my_project = Project.objects.get(id=pk)

    if request.method == "POST":
        my_project.delete()
        return redirect("projects")

    context = {"object": my_project}
    return render(request, "projects/delete_template.html", context)
