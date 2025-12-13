from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from account.models import Customer
from order.models import Cart,CartItems, Order, OrderItems
from product.models import Car
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from order.kafka_producer import run_producer
import datetime
from django.http import JsonResponse, HttpResponseNotAllowed
import random
from django.utils.crypto import get_random_string

# helper method for experiment
def _checkout_cart_and_send_kafka(cart, name, email, phone, address):
    ct = datetime.datetime.now()
    ts = ct.timestamp()

    cart.convertToOrder(
        name=name,
        email=email,
        phone=phone,
        address=address
    )
    cart.is_order = True

    cart_items = cart.cart_items.all()
    for item in cart_items:
        run_producer(
            item.car.title,
            item.car_model,
            item.car_engine,
            item.car_color,
            item.car_price,
            ts,
        )

    cart_items.delete()
    cart.save()
    return ts


# Create your views here.

@login_required(login_url="/accounts/login/")
def get_cart(request):
    cart = None
    try:
        cart = Cart.objects.get(customer = request.user.customer)        
    except Exception as e:
        print(e)

    return render( request,'order/cart.html', context = {'cart' : cart})

@login_required(login_url="/account/login/")
def add_to_cart(request):
    try:
        customer = Customer.objects.get(user_ptr=request.user.id)
        car = request.GET.get('car_id')
        car_model = request.GET.get('car_model')
        car_engine = request.GET.get('car_engine')
        car_color = request.GET.get('car_color')
        car_price = request.GET.get('car_price')
        print("car", car)
        cart , _ = Cart.objects.get_or_create(customer = customer)
        cart_item , _  = CartItems.objects.get_or_create(cart = cart,
                                                          car = Car.objects.get(id = car), car_model=car_model, car_engine=car_engine, car_color=car_color, car_price=car_price)
        print(cart_item)
        cart_item.quantity += 1
        cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    except Exception as e:
        messages.error(request, 'Invalid car ID')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/accounts/login/")
def remove_to_cart(request):
    try:
        customer = Customer.objects.get(user_ptr=request.user.id)
        car = request.GET.get('car_id')

        cart , _ = Cart.objects.get_or_create(customer = customer)
        cart_item   = CartItems.objects.filter(cart = cart , car = Car.objects.get(id = car))
        quantity = request.GET.get('quantity')

        if cart_item.exists():
            cart_item = cart_item[0]

            if quantity:
                cart_item.quantity = int(quantity)
            else:
                cart_item.quantity -= 1

            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    except Exception as e:
        print(e)
        messages.error(request, 'Invalid Product ID')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/accounts/login/")
def checkout_view(request, cart_id):
    cart = Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        _checkout_cart_and_send_kafka(cart, name, email, phone, address)

        return redirect('order-list')

    return render(request, 'order/checkout.html', {'cart': cart})

# original
"""
@login_required(login_url="/accounts/login/")
def checkout_view(request, cart_id):
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    print("timestamp:", ts)
    cart = Cart.objects.get(id=cart_id)


    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        cart.convertToOrder(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        cart.is_order = True

        #newmethod
        cartItems = cart.cart_items.all()
        for item in cartItems:
            # car_title, model, engine, color, price
            # send car details to scheduler via kafka
            run_producer(item.car.title, item.car_model, item.car_engine, item.car_color, item.car_price, ts)
        cart.cart_items.all().delete()
        cart.save()

        return redirect('order-list')

    return render(request, 'order/checkout.html', {'cart': cart})
    """

def order_list_view(request):
    if request.method == 'GET':
        customer = Customer.objects.get(user_ptr=request.user.id)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        print("orders", orders)
        order_items = OrderItems.objects.filter(order__in=orders)
        print("order_items", order_items)
        return render(request, 'order/orders.html', context={'orders':orders, 'order_items':order_items})

@login_required(login_url="/accounts/login/")
def experiment_place_order(request):
    """
    One experiment order:
    - Picks a random car
    - Creates a cart for the logged-in customer
    - Fills it with randomized config data
    - Runs normal checkout logic, including Kafka + timestamp
    - Returns JSON for debugging
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        customer = Customer.objects.get(user_ptr=request.user.id)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found for this user"}, status=400)

    # Get all cars and pick a random one
    cars = list(Car.objects.all())
    if not cars:
        return JsonResponse({"error": "No cars available for experiment"}, status=500)

    car = random.choice(cars)

    # Create a **new cart** for this experiment run
    cart = Cart.objects.create(customer=customer)

    # Randomization helpers
    random_suffix = get_random_string(6)

    engine_options = ["V6", "V8", "Electric", "Hybrid", "Diesel"]
    color_options = ["Red", "Blue", "Black", "White", "Silver", "Green"]

    car_model = getattr(car, "model", f"Model-{random_suffix}")
    car_engine = random.choice(engine_options)
    car_color = random.choice(color_options)

    # Slightly randomize price around the car's real price (if it exists)
    base_price = getattr(car, "price", 100000)
    price_variation = random.randint(-5000, 5000)
    car_price = max(1000, base_price + price_variation)

    # Create the cart item
    cart_item = CartItems.objects.create(
        cart=cart,
        car=car,
        car_model=car_model,
        car_engine=car_engine,
        car_color=car_color,
        car_price=car_price,
        quantity=1,
    )

    print("Experiment: created cart item:", cart_item)


    name = f"Experiment User {random_suffix}"
    email = f"exp{random_suffix.lower()}@example.com"
    phone = str(random.randint(10000000, 99999999))
    address = f"Test Street {random.randint(1, 200)}"

    ts = _checkout_cart_and_send_kafka(
        cart=cart,
        name=name,
        email=email,
        phone=phone,
        address=address,
    )

    order = Order.objects.filter(customer=customer).order_by('-created_at').first()

    return JsonResponse({
        "message": "Experiment order created",
        "timestamp": ts,
        "cart_id": cart.id,
        "order_id": order.id if order else None,
        "car": {
            "id": car.id,
            "title": car.title,
            "model": car_model,
            "engine": car_engine,
            "color": car_color,
            "price": car_price,
        },
})