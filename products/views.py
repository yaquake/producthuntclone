from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.contrib.auth.models import User


def home(request):

    if request.method == 'GET':
        product_cat = request.GET.get('cat', '')
        print(product_cat)
        products = Product.objects.filter(category__contains=product_cat).order_by('-pub_date')
        return render(request, 'products/home.html', {'title': 'Product hunt', 'products': products, 'product_list': product_cat})
    else:
        products = Product.objects.order_by('-pub_date')
        return render(request, 'products/home.html', {'title': 'Product hunt', 'products': products})


@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
           product = Product()
           product.title = request.POST['title']
           product.body = request.POST['body']
           if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
               product.url = request.POST['url']
           else:
               product.url = 'http://' + request.POST['url']
           product.icon = request.FILES['icon']
           product.image = request.FILES['image']
           product.pub_date = timezone.datetime.now()
           product.hunter = request.user
           product.category = request.POST['sel1']
           product.save()
           return redirect('/products/' + str(product.id))

        else:
            return render(request, 'products/create.html', {'error': 'All field are required!', 'title': 'Create a new product'})

    else:
        return render(request, 'products/create.html', {'title': 'Create a new product'})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {"product": product, 'title': 'Product Hunt || ' + product.title})


@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        print(str(User.username))
        if str(User.username) not in product.votenames:
            product.votes_total += 1
            product.votenames += " " + str(User.username)
            product.save()
        return redirect("/products/" + str(product.id))


def search(request):
    if request.method == 'POST':
        what = request.POST['pole']
        where = request.POST['gridRadios']
        if where == "option1":
            result = Product.objects.filter(title__icontains=what)
            return render(request, "products/search.html", {"result": result, 'title': 'Product Hunt || Search',
                                                            'search': "Search result:"})
        if where == "option2":
            result = Product.objects.filter(body__icontains=what)
            return render(request, "products/search.html", {"result": result, 'title': 'Product Hunt || Search',
                                                            'search': "Search result:"})
    else:
        return render(request, "products/search.html", {'title': 'Product Hunt || Search', 'search': ''})







