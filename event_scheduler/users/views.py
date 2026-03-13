# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, CustomUserChangeForm

def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Log the user in automatically after registration
            # login(request, user) 
            return redirect("/api-auth/login/") # Redirect to a 'home' page or login page
    else:
        form = RegisterForm()
    
    return render(request, "registration/signup.html", {"form": form})


def CustomUserChangeView(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: Log the user in automatically after registration
            # login(request, user) 
            return redirect("/") # Redirect to a 'home' page or login page
    else:
        form = CustomUserChangeForm()
    
    return render(request, "registration/signup.html", {"form": form})
