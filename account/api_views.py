from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Registration completed successfully."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("profile")

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            mobile = form.cleaned_data["mobile"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                mobile=mobile,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    "Login successful."
                )

                return redirect("profile")

            else:

                messages.error(
                    request,
                    "Invalid mobile or password."
                )

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


@login_required(login_url="login")
def profile_view(request):

    return render(
        request,
        "profile.html",
        {
            "user": request.user,
        },
    )

@login_required(login_url="login")
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")