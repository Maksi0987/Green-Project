from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect

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