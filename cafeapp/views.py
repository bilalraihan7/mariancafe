from django.shortcuts import render , redirect ,get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import logout
from django.urls import reverse

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
    noofitems=cart.count()
    all_data={'user':user,'food':food, 'cart':cart,'noofitems':noofitems}
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
        staff=Staff.objects.get(id=int(user))
        print(staff)
        new_food = foodmenu(userid=staff, name=name, ftype=ftype, image=image, rate=rate)
        new_food.save()
        
        messages.success(request, 'Food added successfully!')
        return redirect('/staff_home')
    id=request.session['id']
    user=Staff.objects.filter(id=id)
    return render(request, 'cafeapp/add_food.html',{'user':user})

def delete_food(request,id):
    a=foodmenu.objects.get(id=id)
    a.delete()
    return redirect('/staff_home')

def filter(request,fid):
    id=request.session['id']
    user=Staff.objects.filter(id=id)
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



def book_vehicle(request, vehicle_id):
    vehicles = vehicle.objects.get(id=vehicle_id)
    driver = vehicles.userid
    user_id = request.session['id']
    
    if request.method == 'POST':
        pickup_location = request.POST['pickup_location']
        dropoff_location = request.POST['dropoff_location']
        time = request.POST['time']
        date = request.POST['date']
        distance = request.POST['distance']
        user = User.objects.get(id=user_id)
        
        new_booking = booking.objects.create(
            user=user,
            driver=driver,
            vehicle=vehicles,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            time=time,
            date=date,
            distance=distance
        )
        
        vehicles.status = 'booked'
        vehicles.save()
        new_booking.save()
        
        messages.success(request, 'Your booking is confirmed!')
        
        # Redirect to payment page with booking ID
        return redirect(reverse('make_payment', args=[new_booking.id]))
    
    id = request.session['id']
    user = User.objects.filter(id=id)
    context = {'vehicle': vehicle, 'user': user}

    return render(request, 'cafeapp/book_vehicle.html', context)


def view_booking(request):
    id=request.session['id']
    bookings=booking.objects.filter(driver=id)
    user=Driver.objects.filter(id=id)
    all_data={'user':user,'bookings':bookings}
    return render(request,'cafeapp/viewbookings.html',all_data)



def view_drivers(request):
    id = request.session['id']
    user = User.objects.filter(id=id)
    drivers = Driver.objects.all()
    all_data = {'user': user, 'drivers': drivers}
    return render(request, 'cafeapp/drivers.html', all_data)

def my_booking(request):
    id=request.session['id']
    bookings=booking.objects.filter(user=id)
    user=User.objects.filter(id=id)
    all_data={'user':user,'bookings':bookings}
    return render(request,'cafeapp/mybookings.html',all_data)


def view_stats(request):
    countuser=User.objects.count()
    countdrivers=Driver.objects.count()
    countbookings=booking.objects.count()
    cvehicles=vehicle.objects.count()
    bookings = booking.objects.values('vehicle').annotate(total_bookings=Count('vehicle'))
    sorted_bookings = sorted(bookings, key=lambda x: x['total_bookings'], reverse=True)
    most_booked_id = sorted_bookings[0]['vehicle'] if sorted_bookings else None
    most_vehicle=vehicle.objects.filter(id=most_booked_id)


    all={
        'user':countuser,
        'driver':countdrivers,
        'bookings':countbookings,
        'vehicles':cvehicles,
        'most':most_vehicle
    }
    return render(request,'cafeapp/stats.html',all)


def make_payment(request, booking_id):
    if request.method == 'POST':
 
        book = get_object_or_404(booking, id=booking_id)
        payment_amount = book.distance * book.vehicle.rate if book.distance and book.vehicle else 0
        payment = Payment.objects.create(
            bookid=book,
            cname=request.POST.get('cname'),
            amount=payment_amount,
            cardno=request.POST.get('cardno'),
            cvv=request.POST.get('cvv')
        )

        book.payment = payment
        book.save()
        id=request.session['id']
        user = User.objects.filter(id=id)
        return render(request,'cafeapp/success.html',{'user':user})
    else:
        id = request.session['id']
        user = User.objects.filter(id=id)
        book = get_object_or_404(booking, id=booking_id)
        payment_amount = book.distance * book.vehicle.rate if book.distance and book.vehicle else 0
        return render(request, 'cafeapp/payment.html', {'user': user, 'payment_amount': payment_amount})

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