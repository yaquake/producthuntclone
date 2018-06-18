from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.contrib.auth.models import User


def home(request):
    page_quantity = Product.objects.all().count()
    if page_quantity % 5 == 0:
        pages = page_quantity / 5
    else:
        pages = page_quantity // 5 + 1
    list_pages = [x for x in range(1, pages + 1)]
    if request.method == 'GET':
        product_cat = request.GET.get('cat', '')
        # page = request.GET.get('page', '')
        # if page is '':
        #     page = '1'
        # x = int(page)
        products = Product.objects.filter(category__contains=product_cat).order_by('-pub_date') #[5 * (x - 1): 5 * x]
        return render(request, 'products/home.html', {'title': 'Product Finder', 'products': products,
                                                      'product_list': product_cat, 'pages': list_pages})
    else:
        products = Product.objects.order_by('-pub_date')
        return render(request, 'products/home.html', {'title': 'Product Finder', 'products': products,
                                                      'pages': list_pages})


@login_required(login_url="/accounts/login")
def create(request):
    if request.method == 'POST':
        name = request.POST['title']
        if Product.objects.filter(title__icontains=name) is not None:
            create_error = 'A product with "' + name + '" name probably exists'
            return render(request, 'products/create.html', {'title': 'Product Finder || Create a new product',
                                                            'create_error': create_error})

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
            return render(request, 'products/create.html', {'error': 'All field are required!',
                                                            'title': 'Product Finder || Create a new product'})

    else:
        return render(request, 'products/create.html', {'title': 'Product Finder || Create a new product'})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {"product": product, 'title': 'Product Finder || ' + product.title,
                                                    'username': str(User.username)})


@login_required(login_url="/accounts/login")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
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
            return render(request, "products/search.html", {"result": result, 'title': 'Product Finder || Search',
                                                            'search': "Search result:"})
        if where == "option2":
            result = Product.objects.filter(body__icontains=what)
            return render(request, "products/search.html", {"result": result, 'title': 'Product Finder || Search',
                                                            'search': "Search result:"})
    else:
        return render(request, "products/search.html", {'title': 'Product Finder || Search', 'search': ''})











