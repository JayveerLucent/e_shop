from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Categories
from .models.customer import Customer
from .models.orders import Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View

class Index(View):
    
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        print(product)
        # request.session.clear()
        cart = request.session.get('cart')
        
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart
        print("cart ----- ",request.session['cart'])
        return redirect('homepage')
    
    
    
    def get(self, request):
        products = None
        # request.session.clear()
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        
        categories = Categories.get_all_categories()
        print(request.GET)
        category_id = request.GET.get('category_id')
        print("hi---- ",category_id )
        if category_id:
            products = Product.get_all_products_by_category_id(category_id)
        else:
            products = Product.get_all_products()
        data ={}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'index.html', data)

    
def signup(request):
    if request.method ==  'GET':
        print(request.method)
        return render(request, 'signup.html')
    else:
        print(request.method)
        data = request.POST
        
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')
        
        value = {
            'firstname': firstname,
            'lastname' : lastname,
            'phone' : phone,
            'email' : email
        }
        
        if not firstname or not lastname or not email or not phone or not password:
            error = "Input cannot be blank"
            data = {'error': error,
                    'value': value}
            return render(request, 'signup.html', data)
        if len(firstname) < 3 or len(lastname) < 3 or int(phone) <= 999999999 or not len(email) :
            error = "Invalid Input"
            data = {'error': error,
                    'value': value}
            return render(request, 'signup.html', data)
        else:
            password = make_password(password)
            customer = Customer(firstname=firstname, lastname=lastname, phone = phone, email=email , password = password ) 
            customer.registercustomer()
            return render(request, 'registered.html', {'firstname' : firstname})
        
        
#class based views to handle login. Alternative method for defining functions as above
class Login(View):
    return_url= None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self,request):
        email =request.POST.get('email')
        password = request.POST.get('password')
        
        customer = Customer.get_customer_by_email(email)
        print(customer)
        print(email,password)
        if customer is False:
            error = "Customer not Registered, Signup and comeback"
            data = {'error': error,
                    'email': email}
            return  render(request, 'login.html', data)
        else:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['customer_email'] = customer.email
                print(request.session.get('customer_email'), request.session.get('customer_id'))
                print(Login.return_url)
                if Login.return_url:
                    print("1-------------------- ",Login.return_url)
                    if Login.return_url == '/checkout':
                        Login.return_url = '/cart'
                    return HttpResponseRedirect(Login.return_url)
                else:
                    print("2-------------------- ",Login.return_url)

                    Login.return_url=None
                    return redirect('homepage')
            else:
                error = "Invalid Password"
                data = {'error': error,
                    'email': email}
                return  render(request, 'login.html', data)
  
        
def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self , request):
        if request.session.get('cart') is None:
            return render(request, 'cart.html')
        print("cart----- ",request.session.get('cart'))
        print(list(request.session.get('cart').keys()))
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html',{'products':products})

    
class Checkout(View):
    def post(self , request):
        print(request.POST)
        print(request.session.get('customer_id'))

        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer =  request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print("checkout data------ ",customer, phone, address )
        
    
        for product in products:
            order = Order(customer= Customer(id = customer) , product = product, price = product.price, quantity = cart.get(str(product.id)), address = address ,  phone = phone)
            
            print(order)
            order.place_order()
        request.session['cart'] = {}
        return redirect('cart')
    


class ViewOrders(View):
    def get(self, request):
        customer = request.session.get('customer_id')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders':orders})