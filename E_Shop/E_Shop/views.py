from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.middleware.csrf import get_token

from app.models import Catagory, Sub_Category, Product, Contact_Us, Order, Brand
from django.contrib.auth import authenticate,login
from app.models import UserCreateForm
from django.contrib.auth.models import User
# Add to cart
from django.contrib.auth.decorators import login_required
from cart.cart import Cart



def Master(request):
    return render(request,'master.html')

def Index(request):

    catagory = Catagory.objects.all()
    brand = Brand.objects.all()
    brand_id = request.GET.get('brand')

    product = Product.objects.all()
    category_ID = request.GET.get("category")



    if category_ID:
        product = Product.objects.filter(sub_category = category_ID).order_by("-id")

    elif brand_id:
        product = Product.objects.filter(brand = brand_id).order_by("-id")
        
    else:
        catagory = Catagory.objects.all()

    context = {
        'catagory': catagory,
        'product': product,
        'brand': brand,
    }
    return render(request,'index.html',context)

# def set_csrf_cookie(request):
#     response = HttpResponse("CSRF token set.")
#     response.set_cookie("csrftoken", get_token(request))
#     return response

def Signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user=authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserCreateForm()
    context = {
        'form': form,
    }


    return render(request,'registration/signup.html',context)
    


# Add to cart 

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def Contect_Page(request):
    if request.method == 'POST':
        contact = Contact_Us(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        contact.save()
    
    return render(request,'contact.html')

def Checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)

        for i in cart:
            
            temp = cart[i]['price']
            temp_quantity = cart[i]['quantity']
            total = int(temp) * int(temp_quantity)
            order = Order(
                user=user, 
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image = cart[i]['image'],
                address=address,
                phone=phone,
                pincode=pincode,  
                total = total            
            )
            order.save()
        request.session['cart'] = ''
        return redirect('index')
    return HttpResponse("This is ckeckout page")



def Your_Order(request):

    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    
    order = Order.objects.filter(user=user)
    context = {
        'order': order
    }



    return render(request,'order.html',context)



def Product_Page(request):
    catagory = Catagory.objects.all()

    brand = Brand.objects.all()
    brand_id = request.GET.get('brand')

    product = Product.objects.all()
    category_ID = request.GET.get("category")



    if category_ID:
        product = Product.objects.filter(sub_category = category_ID).order_by("-id")

    elif brand_id:
        product = Product.objects.filter(brand = brand_id).order_by("-id")
        
    else:
        catagory = Catagory.objects.all()


    context = {
        'catagory': catagory,
        'brand': brand,
        'product': product
        
    }
    return render(request,'product.html',context)


def Product_Detail(request,id):

    product = Product.objects.filter(id=id).first()
    context = {
        'product': product
    }



    return render(request,'product_detail.html',context)

def Search(request):

    query = request.GET['query']
    product = Product.objects.filter(name__icontains = query)
    context = {
        'product': product
    }


    return render(request,'search.html',context)

