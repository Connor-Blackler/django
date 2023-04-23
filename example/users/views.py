from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile
from .forms import MyCreationForm, EditProfileForm, SkillForm
from .helpers import search_profiles, paginate_profiles

# Create your views here.


def profiles(request):
    my_profiles, search = search_profiles(request)
    custom_range, my_profiles = paginate_profiles(request, my_profiles, 2)

    print(custom_range, my_profiles)
    context = {"profiles": my_profiles,
               "filter": search, "custom_range": custom_range}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk: str):
    my_profile = Profile.objects.get(id=pk)
    descripted_skills = my_profile.skill_set.exclude(description__exact="")
    blank_skills = my_profile.skill_set.filter(description="")

    context = {"profile": my_profile,
               "descripted_skills": descripted_skills, "blank_skills": blank_skills}
    return render(request, 'users/user_profile.html', context)


def login_user(request):
    context = {"page": "login"}

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            new_user = User.objects.get(username=username)
            new_user = authenticate(
                request, username=username, password=password)
            if new_user is not None:
                login(request, new_user)
                return redirect("profiles")
            else:
                messages.error(request, "Username or password is incorrect")
        except:
            messages.error(request, "Username or password is incorrect")

    return render(request, "users/login_register.html", context)


def logout_user(request):
    logout(request)
    messages.info(request, "User was successfully logged out!")
    return redirect("login")


def register_user(request):
    if request.method == "POST":
        form = MyCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was successfully created!")

            login(request, user)
            return redirect("edit-profile")

        else:
            messages.error(
                request, "An error has occurred during registration")

    context = {"page": "register", "form": MyCreationForm()}
    return render(request, "users/login_register.html", context)


@login_required(login_url="login")
def my_profile(request):
    my_profile = request.user.profile
    my_skills = my_profile.skill_set.all()
    projects = my_profile.project_set.all()

    context = {"profile": my_profile,
               "skills": my_skills, "projects": projects}

    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_profile(request):
    form = EditProfileForm(instance=request.user.profile)
    context = {"form": form}

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES,
                               instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("my-profile")

    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    my_profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = my_profile
            skill.save()
            messages.success(
                request, f"'{skill.name}' skill was added successfully")
            return redirect("my-profile")

    context = {"form": form}

    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    my_profile = request.user.profile
    modified_skill = my_profile.skill_set.get(id=pk)
    form = SkillForm(instance=modified_skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=modified_skill)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"'{modified_skill.name}' skill was updated")
            return redirect("my-profile")

    context = {"form": form}

    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    my_profile = request.user.profile
    skill_to_delete = my_profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill_to_delete.delete()
        messages.success(
            request, f"'{skill_to_delete.name}' was successfully deleted")
        return redirect("my-profile")

    context = {"object": skill_to_delete}

    return render(request, "delete_template.html", context)
