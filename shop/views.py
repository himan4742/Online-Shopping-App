from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from . middleware.authentication import authentication_middleware

from .models import Product, Category, Customer, Order


class DetailView(View):
    """."""

    @method_decorator(authentication_middleware)
    def get(self, request):
        """."""

        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        # request.session.clear()
        # if not request.session.get('customer_id'):
        #     error_message = "You are not logged in !!!"
        #     return render(request, "failure.html", {"error": error_message})
        categories = Category.objects.all()
        category_id = request.GET.get("category_id")
        if category_id:
            products = Product.get_all_products_by_category_id(category_id)
        else:
            products = Product.get_all_products()
        context = {"products": products, "categories": categories}
        return render(request, "detail.html", context)

    def post(self, request):
        """."""

        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1

        request.session['cart'] = cart
        print("CART = ", request.session['cart'])
        return redirect("detail")


class SignupView(View):
    """."""

    def get(self, request):
        """."""

        return render(request, 'signup.html')

    def post(self, request):
        """."""

        post_data = request.POST
        first_name = post_data.get('firstname')
        last_name = post_data.get('lastname')
        phone = post_data.get('phone')
        email = post_data.get('email')
        password = post_data.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    @staticmethod
    def validateCustomer(customer):
        error_message = None
        if not customer.first_name:
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'

        return error_message


class LoginView(View):
    """."""

    def post(self, request):
        """."""

        post_data = request.POST
        email = post_data.get("email")
        password = post_data.get("password")
        customer = Customer.objects.filter(email=email)
        login_approval = False
        error_message = None
        if customer:
            login_approval = check_password(password, customer[0].password)
            if login_approval:
                request.session['customer_id'] = customer[0].id
                request.session['email'] = customer[0].email
                return redirect("detail")
            else:
                error_message = "Enter correct password !!!"
        else:
            error_message = "Invalid username or password !!!"
        return render(request, "failure.html", {"error": error_message})


class CartView(View):
    """."""

    def get(self, request):
        """."""

        cart_items = request.session.get("cart")
        if cart_items:
            products = Product.objects.filter(id__in=cart_items.keys())
        else:
            products = Product.objects.none()
        return render(request, "cart.html", {"products": products})


class CheckOutView(View):
    """."""

    def post(self, request):
        """."""

        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer_id')
        customer_email = request.session.get('email')
        cart = request.session.get('cart')
        products = Product.objects.filter(id__in=cart.keys())
        customer_obj = Customer.objects.get(id=customer_id, email=customer_email)

        for product in products:
            order = Order(customer=customer_obj,
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()

        request.session['cart'] = {}

        return redirect("detail")


class OrderView(View):
    """."""

    @method_decorator(authentication_middleware)
    def get(self, request):
        """."""

        customer_id = request.session.get('customer_id')
        orders_created = Order.objects.filter(customer=customer_id).order_by('-date')
        return render(request, 'order.html', {'orders': orders_created})


class LogoutView(View):
    """."""

    def get(self, request):
        """."""

        request.session.clear()
        return redirect("home")
