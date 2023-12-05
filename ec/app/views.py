from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from .models import Cart, Customer, Product, CartItem
from . forms import CustomerRegistrationForm, CustomerProfileForm,MyPasswordChangeForm, OrderPlaceForm, PaymentForm
from django.contrib import messages
from django.db.models import Q, Sum

# Create your views here.

def home(request):
    return render(request,"app/home.html")

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")

def address(request):
        add = Customer.objects.filter(user=request.user)
        return render(request, 'app/address.html',locals())
    
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.province = form.cleaned_data['province']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile has been updated")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
class DeleteAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        add.delete()
        messages.success(request, "Address deleted successfully")
        return redirect("address")

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
             messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())
    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            province = form.cleaned_data['province']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, province=province, zipcode=zipcode)
            reg.save()  # Make sure to call the save method

            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html',locals())
    
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount + 100
    return render(request, 'app/addtocart.html', locals())

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_item = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_item:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 100
        return render(request, 'app/checkout.html', {'add': add, 'cart_item': cart_item, 'totalamount': totalamount})

    def post(self, request):
        # Handling form submission for payment
        selected_address_id = request.POST.get('custid')
        total_amount = request.POST.get('totalamount')

        # Process the payment and other necessary actions here
        
        # Assuming you want to pass some data to the orders.html page
        order_data = {
            'selected_address_id': selected_address_id,
            'total_amount': total_amount,
            # Other data you want to pass to the orders.html
        }

        return render(request, 'app/orders.html', order_data)
    # Redirect to a success page or display order details
    
    
#     def display_orders(request):
#     # Logic para makuha ang cart_items at total_amount
#         cart_items = get_cart_items_somehow()  # Retrieve cart items from your logic or database
#         total_amount = calculate_total_amount()  # Calculate total amount

#         context = {
#         'cart_items': cart_items,
#         'total_amount': total_amount,
#         # Other context variables you might have
#     }

#         return render(request, 'app/orders.html', context)
    
# def get_cart_items_somehow(request):
#     # Kunin ang mga cart items mula sa database na may kaugnayan sa current user
#         cart_items = CartItem.objects.filter(user=request.user)
#         return cart_items

# def calculate_total_amount(cart_items):
#     # Logic para makuha ang total amount mula sa mga cart items
#     total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
#     total_amount += 100  # Dagdag na halaga
#     return total_amount
    
    # def process_payment(request):
    # # Process the form data here

    # # Redirect to the orders.html page after processing the form
    #     return redirect('orders')
   
    

def orders_view(request):
    # Your view logic goes here
    # Fetch the necessary data and render the 'orders.html' template
    return render(request, 'app/orders.html', locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            totalamount = amount + 100
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            totalamount = amount + 100
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')  # Use get() to avoid KeyError if 'prod_id' doesn't exist
        user = request.user

        carts = Cart.objects.filter(product=prod_id, user=user)
        if carts.exists():
            # Decide which cart to delete, here I'm just picking the first one
            cart_to_delete = carts.first()
            cart_to_delete.delete()

            # Recalculate amount and total amount
            cart = Cart.objects.filter(user=user)
            quantity_sum = cart.aggregate(Sum('quantity'))['quantity__sum']
            price_sum = cart.aggregate(Sum('product__discounted_price'))['product__discounted_price__sum']
            
            amount = quantity_sum * price_sum if quantity_sum is not None and price_sum is not None else 0
            totalamount = amount + 100

            data = {
                'quantity': cart_to_delete.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart not found'}, status=404)
        
def payment_view(request):
        user = request.user
        cart = Cart.objects.filter(user=user)
    
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        
        totalamount = amount + 100
        
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                # Your logic for form submission
                pass
        else:
            form = PaymentForm()
        
        context = {
            'form': form,
            'totalamount': totalamount,
        }
        
        return render(request, 'app/payment.html', context)
    
    
def display_orders(request):
    cart_items = get_cart_items_somehow(request)
    total_amount = calculate_total_amount(cart_items)
    
   

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }

    return render(request, 'app/orders.html', context)

def get_cart_items_somehow(request):
    cart_items = Cart.objects.filter(user=request.user)
    return cart_items

def calculate_total_amount(cart_items):
    totalamount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    totalamount += 100
    return totalamount

def checkout_and_order_placement(request):
    if request.method == 'POST':
        form = OrderPlaceForm(request.POST)
        if form.is_valid():
            order_instance = form.save(commit=False)
            # Associate the selected address with the order
            selected_address_id = request.POST.get('custid')  # Fetch selected address ID
            # Associate address with the order_instance
            order_instance.address = AddressModel.objects.get(id=selected_address_id)  # Replace AddressModel with your address model
            order_instance.save()
            return redirect('payment')  # Redirect to payment page
    else:
        form = OrderPlaceForm()
    
    return render(request, 'checkout.html', {'form': form})




        
    
        
        


        
    
    
    
    
 
    
