from django.shortcuts import render , redirect ,get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import logout
from django.urls import reverse
from django.core.paginator import Paginator

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        id_card = request.FILES.get('id_card')
        idnumber = request.POST.get('idnumber')
        if User.objects.filter(email=email).exists():
            msg='User Already Exists'
            return render(request, 'cafeapp/index.html',{'msg':msg})
        else:

            user = User(name=name, email=email,password=password, image=image, address=address,
                        phone=phone,department=department,id_card=id_card)
            user.save()
            messages.success(request, 'User registration successful!')
            return redirect('/')
    else:

        a = foodmenu.objects.all()
        return render(request, 'cafeapp/index.html',{'a':a})
    
def Allfood(request):
    a=foodmenu.objects.all()
    return render(request,'cafeapp/allfood.html',{"a":a})

# def details_vehicle(request,pk):
#     a = vehicle.objects.filter(id=pk)
#     return render(request, 'cafeapp/single_vehicle.html', {"a": a})


def staff_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        license = request.FILES.get('license')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if Staff.objects.filter(email=email).exists():
            msg='User Already Exists'
            return render(request, 'cafeapp/staffreg.html',{'msg':msg})
        else:
        
            staff = Staff(name=name, email=email, license=license, password=password, image=image, address=address, phone=phone)
            staff.save()
            messages.success(request, 'Staff registration successful!')
            return redirect('/')
    else:
        return render(request, 'cafeapp/staffreg.html')


def login(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        obj1 = Staff.objects.filter(email=email, password=password)
        obj2 = User.objects.filter(email=email, password=password)
        if obj1.filter(email=email, password=password).exists():
            for i in obj1:
                id = i.id
                status = i.status
                name=i.name
                request.session['email'] = email
                request.session['password'] = password
                request.session['id'] = id
                request.session['status'] = status
                request.session['name']=name
            # context ={'a': obj }
            if status == 'Verified':
                return redirect('http://127.0.0.1:8000/staff_home')
            else:
                msg='Your Account Verification Is Under Processing'
                return render(request, 'cafeapp/login.html',{'msg2':msg})
        elif obj2.filter(email=email, password=password).exists():
            for i in obj2:
                id = i.id
                name = i.name
                is_verified=i.is_verified
                request.session['name'] = name
                request.session['email'] = email
                request.session['password'] = password
                request.session['id'] = id
                request.session['is_verified'] =is_verified
                if is_verified==True:
                    return redirect('http://127.0.0.1:8000/user_home')
                else:
                    context = {'msg': 'Your Account Verification Is Under Processing'}
                    return render(request,'cafeapp/login.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request,'cafeapp/login.html',context)
    return render(request, 'cafeapp/login.html')

def  view_license(request, id):
    provider = get_object_or_404(Staff, pk=id)
    if provider.license:
        image_path = provider.license.path
        with open(image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'inline; filename={provider.name}_license.jpg'
            return response
    else:
        return HttpResponse('License not found.')
    
def view_user_license(request, id):
    provider = get_object_or_404(User, pk=id)
    if provider.id_card:
        image_path = provider.id_card.path
        with open(image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'inline; filename={provider.name}_license.jpg'
            return response
    else:
        return HttpResponse('License not found.')

def services(request):
    return render(request, 'cafeapp/services.html')

def user_home(request):
    id=request.session['id']
    user=User.objects.filter(id=id)
    food=foodmenu.objects.all()
    cart=Cart.objects.filter(user=id)
    total_amount = sum(item.items.rate * item.quantity for item in cart)
    noofitems=cart.count()
    all_data={'user':user,'food':food, 'cart':cart,'noofitems':noofitems,'total_amount':total_amount}
    return render(request,'cafeapp/user_home.html', all_data )

def logout_view(request):
    logout(request)
    return redirect('/')

def staff_home(request):
    id=request.session['id']
    user=Staff.objects.filter(id=id)
    foods=foodmenu.objects.all()
    all_data={'user':user,'foods':foods}
    return render(request,'cafeapp/staff_home.html', all_data )




def add_food(request):
    if request.method == 'POST':
        name = request.POST['name']
        ftype = request.POST['ftype']
        image = request.FILES['image']
        rate = request.POST['rate']
        user = request.session['id']
        quantity= request.POST['quantity']
        staff=Staff.objects.get(id=int(user))
        print(staff)
        new_food = foodmenu(userid=staff, name=name, ftype=ftype, image=image, rate=rate,quantity=quantity)
        new_food.save()
        
        messages.success(request, 'Food added successfully!')
        return redirect('/staff_home')
    id=request.session['id']
    user=Staff.objects.filter(id=id)
    return render(request, 'cafeapp/add_food.html',{'user':user})

def update_foodDetails(request,foodid):
    if request.method == 'POST':
        name = request.POST.get('name')
        ftype = request.POST.get('ftype')
        image = request.FILES.get('image')
        rate = request.POST.get('rate')
        quantity = request.POST.get('quantity')
        food = foodmenu.objects.get(id=foodid)
        food.name = name
        food.ftype = ftype
        food.rate = rate
        food.quantity = quantity
        if image:
            food.image = image
        food.save()
        return redirect('/staff_home')
    else:
        food = foodmenu.objects.get(id=foodid)
        id=request.session['id']
        user=Staff.objects.filter(id=id)
        all_data={'user':user,'food':food}
        return render(request, 'cafeapp/update_food.html', all_data)
    
    

def delete_food(request,id):
    a=foodmenu.objects.get(id=id)
    a.delete()
    return redirect('/staff_home')

def filter(request,fid):
    id=request.session['id']
    user=User.objects.filter(id=id)
    food=foodmenu.objects.filter(ftype=fid)
    all_data={'user':user,'food':food}
    return render(request,'cafeapp/filtered.html', all_data )


def search_food(request):
    id=request.session['id']
    user=User.objects.filter(id=id)
    name=request.GET.get('name')
    result=foodmenu.objects.filter(name__icontains=name)
    all_data={'user':user,'result':result}
    return render(request,'cafeapp/result.html', all_data )





def my_booking(request):
    id=request.session['id']
    bookings=booking.objects.filter(user=id)
    user=User.objects.filter(id=id)
    all_data={'user':user,'bookings':bookings}
    return render(request,'cafeapp/mybookings.html',all_data)




def edituser(request):
    if request.method == 'POST':
        id = request.session['id']
        user = User.objects.filter(id=id)
        up = User.objects.get(id=id)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if 'image' in request.FILES:
            image = request.FILES['image']
            up.image = image

        up.name = name
        up.address = address
        up.phone = phone
        up.email = email

        up.save()
        ud = User.objects.filter(email=request.session['email'])
        context = {'details': ud,
                   'user': user,
                   'msg': 'Profile Details Updated'}

        return render(request, 'cafeapp/editprofile-user.html', context)
    else:
        id = request.GET.get('id')
        id = request.session['id']
        up = User.objects.filter(id=id)
        user = User.objects.filter(id=id)
        all_data = {
            'user': user,
            'details': up,
        }
        return render(request, 'cafeapp/editprofile-user.html', all_data)

def changepassword_user(request):
    id = request.session['id']
    print(id)
    user = User.objects.filter(id=id)
    all = {
        'user': user,
    }
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print('Email Is:' + email)
        print("Current_password" + str(current_password))
        try:

            ul = User.objects.get(email=email, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                msg =  'Password Changed Successfully'
                all = {
                    'user': user,
                    'msg': msg
                }
                return render(request, 'cafeapp/change_password_user.html',all)
            else:
                context =  'Your Old Password is Wrong'
                all = {
                    'user': user,
                    'msg': context
                }
                return render(request, 'cafeapp/change_password_user.html',all)

        except User.DoesNotExist:
            context =  'Your Old Password is Wrong'
            all = {
                'user': user,
                'msg': context
            }
            return render(request, 'cafeapp/change_password_user.html',all)
    else:
        return render(request, 'cafeapp/change_password_user.html',all)
    

def editstaff(request):
    if request.method == 'POST':
        id = request.session['id']
        user = Staff.objects.filter(id=id)
        up = Staff.objects.get(id=id)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if 'image' in request.FILES:
            image = request.FILES['image']
            up.image = image

        up.name = name
        up.address = address
        up.phone = phone
        up.email = email

        up.save()
        ud = Staff.objects.filter(email=request.session['email'])
        context = {'details': ud,
                   'user': user,
                   'msg': 'Profile Details Updated'}

        return render(request, 'cafeapp/editprofile-driver.html', context)
    else:
        id = request.GET.get('id')
        id = request.session['id']
        up = Staff.objects.filter(id=id)
        user =Staff.objects.filter(id=id)
        all_data = {
            'user': user,
            'details': up,
        }
        return render(request, 'cafeapp/editprofile-driver.html', all_data)

def changepassword_staff(request):
    id = request.session['id']
    print(id)
    user = Staff.objects.filter(id=id)
    all = {
        'user': user,
    }
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print('Email Is:' + email)
        print("Current_password" + str(current_password))
        try:

            ul = Staff.objects.get(email=email, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                msg =  'Password Changed Successfully'
                all = {
                    'user': user,
                    'msg': msg
                }
                return render(request, 'cafeapp/change_password_driver.html',all)
            else:
                context =  'Your Old Password is Wrong'
                all = {
                    'user': user,
                    'msg': context
                }
                return render(request, 'cafeapp/change_password_driver.html',all)

        except Staff.DoesNotExist:
            context =  'Your Old Password is Wrong'
            all = {
                'user': user,
                'msg': context
            }
            return render(request, 'cafeapp/change_password_driver.html',all)
    else:
        return render(request, 'cafeapp/change_password_driver.html',all)
    

    
def addToCart(request, food_id):
    user_id = request.session.get('id')
    user = get_object_or_404(User, id=user_id)
    food = get_object_or_404(foodmenu, id=food_id)
    if Cart.objects.filter(user=user, items=food).exists():
        messages.error(request, 'Item already in cart!')
    else:
        cart = Cart.objects.create(user=user, items=food)
        cart.save()
    return redirect('/user_home')

def removeFromCart(request, food_id):
    user_id = request.session.get('id')
    user = get_object_or_404(User, id=user_id)
    food = get_object_or_404(foodmenu, id=food_id)
    cart = Cart.objects.get(user=user, items=food)
    cart.delete()
    return redirect('/user_home')


def checkout(request):
    user_id = request.session.get('id')
    user = User.objects.filter(id=user_id)
    cart = Cart.objects.filter(user=user_id)
    total_amount = sum(item.items.rate * item.quantity for item in cart)
    request.session['total_amount'] = total_amount
    return render(request, 'cafeapp/payment.html', {'cart': cart, 'total_amount': total_amount, 'user': user})

def payment(request):
    if request.method == 'POST':
        user_id = request.session.get('id')
        user = get_object_or_404(User, id=user_id)
        total_amount = request.session.get('total_amount')
        cname = request.POST.get('cname')
        cardno = request.POST.get('cardno')
        cvv = request.POST.get('cvv')
        payment = Payment.objects.create(user=user, cname=cname, amount=total_amount, cardno=cardno, cvv=cvv)
        payment.save()
        messages.success(request, 'Payment successful!')
        return redirect('/confirm_checkout')
    else:
        total_amount = request.session.get('total_amount')
        return render(request, 'payment.html', {'total_amount': total_amount})

def confirm_checkout(request):
    try:
        user_id = request.session.get('id')
        user = get_object_or_404(User, id=user_id)
        total_amount = request.session.get('total_amount')
        cart = Cart.objects.filter(user=user)
        
        # Create a new Checkout instance
        checkout = Checkout.objects.create(user=user, total_amount=total_amount)
        for item in cart:
            checkout.items.add(item.items)
            # Reduce the quantity of the food item from menu model
            food = foodmenu.objects.get(id=item.items.id)
            food.quantity -= item.quantity
            food.save()
        checkout.save()
        cart.delete()  # Delete the cart items
        messages.success(request, 'Checkout successful!')
    except Exception as e:
        messages.error(request, f'Error occurred during checkout: {str(e)}')
    return redirect('/mybookings')


from django.http import JsonResponse

def increaseQuantity(request, food_id):
    user_id = request.session.get('id')
    user = get_object_or_404(User, id=user_id)
    food = get_object_or_404(foodmenu, id=food_id)
    cart = Cart.objects.get(user=user, items=food)
    
    # Check if increasing quantity exceeds available quantity
    if cart.quantity + 1 > food.quantity:
        messages.error(request, 'Exceeds available quantity!')
        return redirect('/user_home')
    cart.quantity += 1
    cart.save()
    return redirect('/user_home')


def decreaseQuantity(request, food_id):
    user_id = request.session.get('id')
    user = get_object_or_404(User, id=user_id)
    food = get_object_or_404(foodmenu, id=food_id)
    cart = Cart.objects.get(user=user, items=food)
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()
    return redirect('/user_home')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import User, Checkout  # Ensure to import your models

def myBookings(request):
    user_id = request.session.get('id')
    useri = get_object_or_404(User, id=user_id)  # This gets the user object
    bookings = Checkout.objects.filter(user=useri).order_by('-checkout_date')  # Filter bookings for this user
    user=User.objects.filter(id=user_id)
    page_number = request.GET.get('page', 1)  # Get the page number from the request
    paginator = Paginator(bookings, 4)  # Show 5 bookings per page

    try:
        bookings_page = paginator.page(page_number)
    except PageNotAnInteger:
        bookings_page = paginator.page(1)
    except EmptyPage:
        bookings_page = paginator.page(paginator.num_pages)

    # Now, pass the paginated page object under the key 'bookings'
    return render(request, 'cafeapp/mybookings.html', {'bookings': bookings_page, 'user': user})


def viewBookingsStaff(request):
    staff_id = request.session.get('id')
    user = Staff.objects.filter(id=staff_id)
    bookings_list = Checkout.objects.all().order_by('-checkout_date')

    # Set up pagination
    paginator = Paginator(bookings_list, 5)  # Show 5 bookings per page
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)

    return render(request, 'cafeapp/viewbookings.html', {'bookings': bookings, 'user': user})

from collections import Counter
from django.db.models import Prefetch, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

# Assuming the existence of Checkout and foodmenu models
def viewStatistics(request):
    staff_id = request.session.get('id')
    user = Staff.objects.filter(id=staff_id)

    # Get checkouts and common combos
    checkouts = Checkout.objects.prefetch_related(
        Prefetch('items', queryset=foodmenu.objects.all())
    )

    combo_counter = Counter()

    for checkout in checkouts:
        items = checkout.items.all()
        combo = tuple(sorted([item.id for item in items]))
        if combo:
            combo_counter[combo] += 1

    most_common_combos = combo_counter.most_common(5)  # Fetch more combos

    combo_data = []
    for combo, count in most_common_combos:
        item_names = foodmenu.objects.filter(id__in=combo).values_list('name', flat=True)
        combo_name = ', '.join(item_names)
        combo_data.append({'combo': combo_name, 'count': count})

    # Get month-wise booking list for the last 3 months
    three_months_ago = timezone.now() - timedelta(days=90)
    monthwise_bookings = Checkout.objects.filter(checkout_date__gte=three_months_ago).annotate(
        month=TruncMonth('checkout_date')
    ).values('month').annotate(count=Count('id')).order_by('month')

    # Format the monthwise bookings for display
    monthwise_booking_data = [
        {'month': booking['month'].strftime("%B %Y"), 'count': booking['count']}
        for booking in monthwise_bookings
    ]
    print(monthwise_booking_data)

    context = {
        'user': user,
        'combo_data': combo_data,
        'monthwise_booking_data': monthwise_booking_data,
    }

    return render(request, 'cafeapp/viewstats.html', context)
