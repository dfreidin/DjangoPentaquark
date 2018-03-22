# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms, authenticate, login as auth_login, logout as auth_logout
from .models import *

# Create your views here.
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect(pentaquark)
        return render(request, "users/login.html")
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            auth_login(request, user)
            return redirect(petaquark)
    return redirect(register)

def register(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect(pentaquark)
        form = auth_forms.UserCreationForm()
        return render(request, "users/register.html", {"form": form})
    if request.method == "POST":
        form = auth_forms.UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            auth_login(request, new_user)
            return redirect(pentaquark)
        return redirect(register)

@login_required(login_url=login)
def logout(request):
    auth_logout(request)
    return redirect(login)

@login_required(login_url=login)
def pentaquark(request):
    game = GameLogic(request.user)
    return render(request, "game/pentaquark.html")