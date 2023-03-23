from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.views import View
from apps.home.models import Product
from shop.models import *
from django.shortcuts import render, get_object_or_404
from shop.forms import *
from wallet.models import *
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal


# Create your views here.
class shop(View):
    template_name = 'shop/product_list.html'
    context = {}

    def get(self, request):
        product = Product.objects.all()
        context ={
            'products':product
        }
        return render(request,self.template_name,context)



def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    user = request.user
    
    # Check if the product is in stock
    if product.stock > 0:
        cart1, _ = cart.objects.get_or_create(user=user, is_paid=False)
        cart_item, created = CartItems.objects.get_or_create(product=product, cart=cart1)
        
        # Check if the cart item quantity is less than the product stock
        if cart_item.quantity < product.stock:
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        else:
            messages.error(request, f"Sorry, the stock for {product.name} is currently insufficient.")
    else:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





def product_detail(request, id):
    products = Product.objects.get(id=id)
    context = {'product': products}
    return render(request, 'shop/product_detail.html', context)


def remove_cart(request, id):
    try:
        cart_item = CartItems.objects.get(product_id=id)
        messages.success(request, f" {cart_item.product.name} is sucessfully removed from the cart.")
        cart_item.delete()
    except Exception as e:
        print(e,"=============================================================" ,id)
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class cart_view(View):
    def get(self,request):
        user = request.user
        try:
            user_cart = cart.objects.get(user=user)
        except cart.DoesNotExist:
            return render(request, 'shop/cart.html')

        cart_items = user_cart.items.all()
        total_price = user_cart.get_cart_total()
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'shop/cart.html', context)
    
def UpdateCart(request):
    if request.method == 'POST':

        prod_id = int(request.POST.get('prod_id'))
        quantity = int (request.POST.get('quantity'))
        user_cart = cart.objects.get(user=request.user)
        user_cart.items.filter(product=prod_id).update(quantity=quantity)
    return redirect('cart')




class CheckoutAddress(View):
    template_name ='shop/checkout_address.html'
    context = {}
    def get(self, request, *args, **kwargs):
        context ={ 'form' : address_form()}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = address_form(request.POST)
        if form.is_valid():
             address = form.save(commit=False)
             address.user = request.user
             address.save()
             total1 = cart.objects.filter(user=request.user).values_list('total', flat=True).first()
                

             order = Orders.objects.create(user=request.user, address=address, total = total1 )
             if request.user.cart:
                 cart_id = request.user.cart.values('id').first()['id']
                 cart_items = CartItems.objects.filter(cart_id = cart_id).all()
                 product = Product.objects.all()
                 for item in cart_items:
                     product = Product.objects.filter(id=item.product_id).first()
                     Order_items.objects.create(order=order, product=product.name, quantity=item.quantity, price=item.get_product_price())
                #  cart_items.delete()
                #  product.stock -= item.quantity
                #  product.save()
        return redirect('checkout_payment')



class CheckoutPayment(View):
    template_name ='shop/checkout_payment.html'
    context = {}
    wallet = UserWallet.objects.all()

    def get(self, request, *args, **kwargs):
        total1 = cart.objects.filter(user=request.user).values_list('total', flat=True).first()
        wallet = UserWallet.objects.get(user=request.user).balance
        walletbalance = wallet - total1
        context = {
            'form' : payment_form(),
            'wallet' : wallet,
            'balance' : walletbalance
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = payment_form(request.POST)
        total1 = cart.objects.filter(user=request.user).values_list('total', flat=True).first()
        if form.is_valid():
            if form.cleaned_data['payment_type'] == '1':
                # Process payment via wallet
                wallet = UserWallet.objects.get(user=request.user)
                if wallet.balance > total1:
                    wallet.balance = wallet.balance - total1
                    wallet.save()
                    order = Orders.objects.filter(user=request.user).last()
                    order.status = "fullfilled"
                    order.save()
                    if request.user.cart:
                        cart_id = request.user.cart.values('id').first()['id']
                        cart_items = CartItems.objects.filter(cart_id = cart_id).all()
                        product = Product.objects.all()
                        for item in cart_items:
                            product = Product.objects.filter(id=item.product_id).first()
                            cart_items.delete()
                            product.stock -= item.quantity
                            product.save()
                    return render(request, 'shop/checkout_success.html', {'order': order})
                else:
                    messages.error(request,"insufficient balance")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                   
            elif form.cleaned_data['payment_type'] == '2':
                # Process payment via coupon code
                code = request.POST['fname']
                try:
                    coupon = Coupon.objects.get(code=code)
                    if coupon.expiration_date < timezone.now().date():
                       messages.error(request, "Coupon has expired.")
                       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    else:
                        coupon.discount_amount  -= total1
                        coupon.save()
                        order = Orders.objects.filter(user=request.user).last()
                        order.status = "fullfilled"
                        order.save()
                        if request.user.cart:
                            cart_id = request.user.cart.values('id').first()['id']
                            cart_items = CartItems.objects.filter(cart_id = cart_id).all()
                            product = Product.objects.all()
                            for item in cart_items:
                                product = Product.objects.filter(id=item.product_id).first()
                                cart_items.delete()
                                product.stock -= item.quantity
                                product.save()
                        return render(request, 'shop/checkout_success.html', {'order': order})
                except Coupon.DoesNotExist:
                   messages.error(request, "Invalid Coupon Code")
                   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
            else:
                # Invalid payment type
                error_message = "Invalid payment type."
                return render(request, 'shop/checkout_success.html', {'form': form, 'error_message': error_message})




   
