from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import MyCreationForm

# Create your views here.
def profiles(request):
    my_profiles = Profile.objects.all()
    context = {"profiles": my_profiles}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk: str):
    my_profile = Profile.objects.get(id=pk)
    descripted_skills = my_profile.skill_set.exclude(description__exact="")
    blank_skills = my_profile.skill_set.filter(description="")

    context = {"profile": my_profile,
               "descripted_skills": descripted_skills, "blank_skills": blank_skills}
    return render(request, 'users/user-profile.html', context)


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
            return redirect("profiles")

        else:
            messages.error(
                request, "An error has occurred during registration")

    context = {"page": "register", "form": MyCreationForm()}
    return render(request, "users/login_register.html", context)
