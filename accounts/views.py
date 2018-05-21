from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        #   Button pressed
        if request.POST['password1'] == request.POST['password2']:
            if 8 <= len(request.POST['password1']) <= 20:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    auth.login(request, user)
                    return redirect('home')
            else:
                return render(request, 'accounts/signup.html', {'error': 'Password must be between 8 and 20 letters.'})

        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match'})

    else:
        # User wants to enter
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect'})

    else:
        return render(request, 'accounts/login.html')


def logout(request):
    # TODO need to route to homepage
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    else:
        return render(request, 'accounts/signup.html')