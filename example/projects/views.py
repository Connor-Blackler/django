from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .helpers import search_projects, paginate_projects


def projects(request):
    my_projects, search = search_projects(request)
    custom_range, my_projects = paginate_projects(request, my_projects, 6)

    context = {"projects": my_projects, "filter": search,
               "custom_range": custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    review_form = ReviewForm()

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        review = review_form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.update_vote_count()
        messages.success(request, "Successfully added your review!")

        return redirect("project", pk=project_obj.id)

    return render(request, 'projects/single-projects.html',
                  {"project": project_obj, "review_form": review_form})


@ login_required(login_url="login")
def create_project(request):
    my_form = ProjectForm()
    my_profile = request.user.profile

    if request.method == "POST":
        new_tags = request.POST.get("new_tags").replace(",", " ").split()
        my_form = ProjectForm(request.POST, request.FILES)
        if my_form.is_valid():
            new_project = my_form.save(commit=False)
            new_project.owner = my_profile
            new_project.save()
            for my_tag in new_tags:
                my_tag, create = Tag.objects.get_or_create(name=my_tag)
                new_project.tags.add(my_tag)
            return redirect("my-profile")

    context = {"form": my_form}
    return render(request, "projects/project_form.html", context)


@ login_required(login_url="login")
def update_project(request, pk):
    my_profile = request.user.profile
    my_project = my_profile.project_set.get(id=pk)

    my_form = ProjectForm(instance=my_project)

    if request.method == "POST":
        new_tags = request.POST.get("new_tags").replace(",", " ").split()
        print(new_tags)
        my_form = ProjectForm(request.POST, request.FILES, instance=my_project)
        if my_form.is_valid():
            new_project = my_form.save()
            for my_tag in new_tags:
                my_tag, create = Tag.objects.get_or_create(name=my_tag)
                new_project.tags.add(my_tag)

            new_project.save()
            return redirect("my-profile")

    context = {"form": my_form, "project": my_project}
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
