from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from feane.models import Order, OrderItem, Posts,Category,Product, Product_Category, ShippingDetails
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from feane.models import Book_table
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
# from imageai.Classification import ImageClassification
# from django.core.mail import send_mail
# from feaneproject.settings import EMAIL_HOST_USER


# Create your views here.

# function for home page 
def index(request):
    #posts with 'slider' category
    slider_category = Category.objects.get(title='slider')
    sliders = Posts.objects.filter(category=slider_category)
    #print(sliders)
    
    # products with 'menu' category
    product_category = Product_Category.objects.get(name='Menu')
    products = Product.objects.filter(product_category=product_category)
    content_type = Product.objects.values('content_type').distinct()
   

    # post with 'about' category
    category = Category.objects.get(title='about')
    about = Posts.objects.filter(category=category)

    # post with 'customer' category
    category = Category.objects.get(title='customer')
    customer = Posts.objects.filter(category=category)

    #for getting cart count 
    cart_count = get_cart_count(request)

    #for getting the offer price 
    products_offer = Product.objects.order_by('-offer_percentage')[:2]

    context ={
        "sliders ": sliders,  
        "products": products,
        "content type" : content_type,
        "about" :about,
        'category':category,
        "customer":customer,
        "content_type":content_type,
       "cart_count": cart_count,
       "products_offer":products_offer
    }
    return render(request, 'index.html',context)

#for keeping the cart count on the icon
def get_cart_count(request):
    cart = request.session.get('cart', {})
    return sum(cart.values())

# for about page
def about(request):
    category = Category.objects.get(title='about')
    about = Posts.objects.filter(category=category)
    cart_count = get_cart_count(request)
    context ={
        "about":about,
        'category':category,
        "cart_count": cart_count
    }
    return render(request ,'about.html',context)

# for menu page
def menu(request):
    
    # products with 'menu' category
    product_category = Product_Category.objects.get(name='Menu')
    products = Product.objects.filter(product_category=product_category)
    content_type = Product.objects.values('content_type') .distinct()
    cart_count = get_cart_count(request)
    context ={
        "product_category":product_category,
        "products":products,
        "content_type":content_type,
        "cart_count": cart_count
    }
    return render(request ,'menu.html',context) 

# for book table 
@csrf_exempt
def book_table(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        num_of_persons = int(request.POST.get('num_of_persons'))
        date =datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date() 

        if not all([name, number, email, num_of_persons, date]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        Book_table.objects.create(
            name=name,
            number=number,
            email=email,
            num_of_persons=num_of_persons,
            date=date
        )
        
        return JsonResponse({'message': 'Table booked successfully!'})
    else:
        cart_count = get_cart_count(request)
        context = {
            'cart_count': cart_count
        }
        return render(request, 'book.html',context )

# for showing item count on navbar cart icon 
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

        # Add to the cart in session
        cart = request.session.get('cart', {})
        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

        request.session['cart'] = cart
 
        # Calculate the total cart count
        cart_count = sum(cart.values())

        return JsonResponse({
            'success': True,
            'cart_count': cart_count
        })

    return JsonResponse({'success': False, 'error': 'Invalid method'})

# for viewing added list on cart page
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = [{'id': key, 'quantity': value} for key, value in cart.items()]
    products = Product.objects.filter(id__in=cart.keys())
    cart_count = get_cart_count(request)
    


    for item in cart_items:
        product = products.get(id=item['id'])
        item['product'] = product
        item['total_price'] = product.price * item['quantity']

    subtotal = sum(item['total_price'] for item in cart_items)
    subtotal_formatted = "{:.2f}".format(subtotal)

    context = {
        'cart_items': cart_items,
        'cart_count':cart_count,
        'subtotal': subtotal_formatted
    }
    return render(request, 'cart.html', context)

#for removing cart item
def remove_from_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        cart = request.session.get('cart', {})

        if item_id in cart:
            del cart[item_id]
            request.session['cart'] = cart
            return JsonResponse({'success': True, 'message': 'Item removed successfully!'})

        return JsonResponse({'success': False, 'message': 'Item not found in cart!'})

    return JsonResponse({'success': False, 'message': 'Invalid method'})

#for editing cart item
@csrf_exempt
def edit_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('new_quantity'))

        cart = request.session.get('cart', {})
        if item_id in cart:
            cart[item_id] = new_quantity
            request.session['cart'] = cart

            product = Product.objects.get(id=item_id)
            updated_total_price = product.price * new_quantity

            return JsonResponse({'success': True, 'message': 'Quantity updated successfully!','updated_total_price': "{:.2f}".format(updated_total_price)})

        return JsonResponse({'success': False, 'message': 'Item not found in cart!'})

    return JsonResponse({'success': False, 'message': 'Invalid method'})

#for user registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'register.html',{'form':form})

#for order checkout
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = [{'id': key, 'quantity': value} for key, value in cart.items()]
    products = Product.objects.filter(id__in=cart.keys())
    
    for item in cart_items:
        product = products.get(id=item['id'])
        item['product'] = product
        item['total_price'] = product.price * item['quantity']

    subtotal = sum(item['total_price'] for item in cart_items)
    subtotal_formatted = "{:.2f}".format(subtotal) 
    
    if request.method == 'POST':
        # Extract shipping information from the POST data
        full_name = request.POST['full_name']
        address = request.POST['address']
        city = request.POST['city']
        postal_code = request.POST['postal_code']
        phone_number = request.POST['phone_number']

        # Save the shipping details to the database
        shipping_details = ShippingDetails(
            full_name=full_name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone_number=phone_number
        )
        shipping_details.save()
        
        # Create an order with user, subtotal, and the saved shipping details
        order = Order(
            user=request.user,
            subtotal=subtotal, 
            shipping_details=shipping_details
            )
        order.save()

        # subject = 'Order Receipt'
        # message = 'Thank you for your order. Your order details are as follows:\n\n'

        # Save the individual items in the order
        for item in cart_items:
            order_item = OrderItem(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                total_price=item['total_price']
            )
            order_item.save()
        #     message += f"{item['product'].title} - Quantity: {item['quantity']} - Total: ${item['total_price']:.2f}\n"

        # # Clear the cart after checkout
        request.session['cart'] = {}
        # message += f"\nSubtotal: ${subtotal}\n"
        # message += f"\nShipping Address:\n{full_name}\n{address}\n{city}\n{postal_code}\nPhone: {phone_number}"
        # subject="send mail"
        # sender = settings.EMAIL_HOST_USER
        # receivers = [request.user.email, 'jishamdigitz@gmail.com']  # Send to user and admin

        # send_mail(subject, message, sender, receivers)
        messages.success(request, 'Order placed successfully!')

        return redirect('index') 
       

        
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal_formatted
    }

    return render(request, 'checkout.html', context)

#for user login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('view_cart')  # Redirect to homepage or any other page after successful login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

#for user logout
def user_logout(request):
    logout(request)
    return redirect('index')

# for image Ai section
# def my_aipage(request): 


#     execution_path = os.getcwd()

#     prediction = ImageClassification()
#     prediction.setModelTypeAsResNet50()
#     prediction.setModelPath(os.path.join(execution_path, "resnet50-19c8e357.pth"))
#     prediction.loadModel()

#     predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, "cat.jpg"), result_count=5 )
#     for eachPrediction, eachProbability in zip(predictions, probabilities):
#         print(eachPrediction , " : " , eachProbability)
#     return render(request, 'imageprediction.html')                       

