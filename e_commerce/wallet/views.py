from decimal import Decimal
from django.shortcuts import render, redirect
from apps.authentication.models import CustomUser
from .models import UserWallet
from django.contrib.auth.decorators import login_required
import random, string
from decimal import Decimal
from django.utils import timezone
from .models import Coupon
from django.contrib import messages
# Create your views here.

@login_required(login_url="/login/")
def FundDeposit(request):
    msg=""
    if request.method == 'POST' :
       try:
           amount = request.POST["amount"]
           senderUser= CustomUser.objects.get(username=request.user.username)
           userget = UserWallet.objects.get(user= senderUser)
           userget.balance += Decimal(amount)
           
           userget.save()
           messages.success(request, "Fund successfully added")
           return redirect ('home')
       except Exception as e:
           messages.error(request, "Failed to deposit Fund")
           return render(request,'home/fund-deposit.html')
    return render(request,'home/fund-deposit.html')       

#          -------------------------------------- coupon generation function -----------------------------------

@login_required(login_url="/login/")
def GenerateCoupons(request):

    if request.method == 'POST':
        getUser= CustomUser.objects.get(username=request.user.username)
        deductamount = UserWallet.objects.get(user = getUser) 
        discount_amount = request.POST['discount_amount']
        expiration_date = request.POST['expiration_date']
        if deductamount.balance > Decimal (discount_amount):
            deductamount.balance -= int(discount_amount)
            deductamount.save()
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            coupon = Coupon(code=code, discount_amount=discount_amount, expiration_date=expiration_date)
            messages.success(request, "coupon generated")
            coupon.save()
            return redirect('coupon_list')
        else:
            messages.error(request, "coupon amount is greater than wallet balance")
            return render(request, 'home/generate_coupon.html')

    return render(request, 'home/generate_coupon.html')



def CouponList(request):
    coupons = Coupon.objects.all()
    context = {'coupons': coupons, 'segments': 'coupon'}
    return render(request, 'home/coupon_list.html',context )

def use_coupon(request, coupon_id):
    coupon = Coupon.objects.get(pk=coupon_id)
    coupon.is_used = True
    coupon.save()
    return redirect('coupon_list')

def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(pk=coupon_id)
    coupon.delete()
    return redirect('coupon_list')
