from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from products.models import Product


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            if 8 <= len(request.POST['password1']) <= 20:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'accounts/signup.html', {'error': 'Username has already been taken',
                                                                    'title': 'Sign up'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    auth.login(request, user)
                    return redirect('home')
            else:
                return render(request, 'accounts/signup.html', {'error': 'Password must be between 8 and 20 letters.',
                                                                'title': 'Sign up'})

        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match', 'title': 'Sign up'})

    else:
        return render(request, 'accounts/signup.html', {'title': 'Sign up'})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect',
                                                           'title': 'Login'})

    else:
        return render(request, 'accounts/login.html', {'title': 'Login'})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    else:
        return render(request, 'accounts/signup.html')


def userdetail(request):
    user = User.objects.get(username=request.user.username)
    product = Product.objects.filter(hunter__username=user.username).order_by('id')
    return render(request, "accounts/userinfo.html", {'product': product, 'title': 'Product Finder || User info'})
