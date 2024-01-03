from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from home.forms.user_form import CustomAuthenticationForm, RegisterForm, RegisterUpdateForm, PasswordUpdateForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from home.models import Profile


@login_required(login_url='home:login')
def index(request):
    User = get_user_model()
    users = User.objects.all()

    return render(
        request,
        'user/list.html',
        {
            'usuarios': users
        }
    )

def login(request):
    form = CustomAuthenticationForm(request)

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)

            # Validando se já alterou senha uma vez
            try: 
                Profile.objects.get(user=user).force_password_change = True
            except Profile.DoesNotExist:
                return redirect('home:change_password')
        
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('home:index')
        messages.error(request, 'Login inválido')

    return render(
        request,
        'user/login.html',
        {
            'form': form
        }
    )

def logout(request):
    auth.logout(request)
    return redirect('home:login')

@login_required(login_url='home:login')
def update(request):

    UserTable = get_user_model()
    user = UserTable.objects.get(pk=pk)

    form = RegisterUpdateForm(instance=user)

    return render(
        request,
        'user/edit.html',
        {
            'form': form
        }
    )


# @login_required(login_url='home:login')
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado')
            return redirect('home:login')

    return render(
        request,
        'user/register.html',
        {
            'form': form
        }
    )

@login_required(login_url='home:login')
def change_password(request):
    user = get_object_or_404(User, id=request.user.id)
    form = PasswordUpdateForm(instance=user)

    if request.method == 'POST':
            form = PasswordUpdateForm(request.POST)

            if form.is_valid():
                user.set_password(request.POST.get('password1'))
                user.save()

                profile_instance = Profile(user=user, force_password_change=True)
                profile_instance.save()

                messages.success(request, 'Senha Alterada')
                return redirect('home:login')

    return render(
        request,
        'user/change_password.html',
        {
            'form': form
        }
    )
