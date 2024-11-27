from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import User, UserGroup, UserAlias


@login_required()
def index(request):
    groups = UserGroup.objects.all()
    return render(request, "splitwise_clone/index.html", {"groups": groups})


@login_required()
def create_group(request):
    if request.method == "POST":
        participants = []
        group_name = request.POST.get("group_name")
        participantIterator = 0
        participant = request.POST.get(f"participant-{participantIterator + 1}", None)
        while participant:
            participants.append(participant)
            participantIterator = participantIterator + 1
            participant = request.POST.get(f"participant-{participantIterator + 1}", None)

        group = UserGroup(name=group_name)
        group.save()
        created_group = UserGroup.objects.get(name=group_name)
        user_aliases = []
        for participant in participants:
            user_aliases.append(UserAlias(alias=participant, group=created_group))
        UserAlias.objects.bulk_create(user_aliases)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "splitwise_clone/create-group.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "splitwise_clone/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "splitwise_clone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "splitwise_clone/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "splitwise_clone/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "splitwise_clone/register.html")
