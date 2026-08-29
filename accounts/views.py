from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserEditForm, ProfileEditForm
from main.models import Category

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return redirect('main:product_list')
    else:
        auth_form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {'form': auth_form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:product_list')

    if request.method == 'POST':
        reg_form = UserCreationForm(data=request.POST)
        if reg_form.is_valid():
            new_user = reg_form.save()
            login(request, new_user)
            return redirect('main:product_list')
    else:
        reg_form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': reg_form})

def logout_view(request):
    if request.method == 'POST' or request.user.is_authenticated:
        logout(request)
    return redirect('main:product_list')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ваш профіль успішно оновлено!")
            return redirect('accounts:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'categories': categories,
        'title': 'Редагування профілю'
    }
    return render(request, 'accounts/profile_edit.html', context)