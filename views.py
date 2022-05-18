from django.shortcuts import render,redirect
from turfapp import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout,login as authlogin
import random
from django.contrib.auth import logout
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control

# Create your views here.

def home(request):

    offer = models.Offer.objects.filter(closed = False).order_by('-bdate')[:6]
    feedobject = models.Feedback.objects.all()[:6]
    return render(request, 'turfapp/index.html',{'offers' :offer,  'feedobjects': feedobject})

@login_required
def book(request):
    current_date = datetime.datetime.now().date()
    if request.method == 'GET':
        date_search = request.GET.get('search_date')
        if date_search:
            current_date = date_search

    booked_slots = models.Booking.objects.filter(date = current_date)
    slot_list = []
    for slot in booked_slots:
        slot_list.append(slot.slot.id)
    print('date', str(current_date) , str(datetime.datetime.now().date()))
    if str(datetime.datetime.now().date()) == str(current_date):
        print('+'*100)
        slot = models.Slot.objects.filter(time__gt = datetime.datetime.now().time()).exclude(id__in = slot_list).order_by('time')
    else:
        print('esle')
        slot = models.Slot.objects.all().exclude(id__in=slot_list).order_by('time')

    return render(request, 'turfapp/book.html',{'slots' :slot, 'current_date' :str(current_date)})

# @login_required
# def order(request):
#
#     transaction = models.Transaction.objects.all()
#     return render(request,'turfapp/index.html',{'transactions' :transaction})

# def login(request):
#
#
#     return render()

def changepassword(request):

    return render()

def coin(request):

    return render()

def login(request):

    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #

    return render(request,'turfapp/login.html')


def create_refcode(user):
    while True:
        user = user[:4]
        random_ind = random.randint(0,999)
        ref_code = user+str(random_ind)
        user_ref = models.UserDetail.objects.filter(ref_code = ref_code )
        if len(user_ref) ==  0:
            break
    return ref_code

@cache_control(no_cache = True, must_revalidate = True , no_store = True)
def signup(request):
    if request.method == 'POST':
        print('reach')
        phonenumber = request.POST['phonenumber']
        password = request.POST['password']
        emailid = request.POST['emailid']
        name = request.POST['name']
        address = request.POST['address']
        referral = request.POST['referral']
        exist_user = models.User.objects.filter(username = phonenumber)
        if len(exist_user)>0:
            messages.error(request,'phone number already registered')
            return render(request, 'turfapp/signup.html')
        else:
            num_ref = models.Settings.objects.first()
            if len(referral )> 0:
                try:
                    ref_userobject = models.UserDetail.objects.filter(ref_code = referral).first()
                    ref_userobject.coin_balance = ref_userobject.coin_balance + num_ref.coinsper_ref
                    ref_userobject.save()
                    ref_obj = models.Referrals(parent=ref_userobject.user, child=name,
                                               coins_earned=num_ref.coinsper_ref)
                    ref_obj.save()
                except Exception as e:
                    messages.error(request, 'referral code doesnot exist')
                    return render(request, 'turfapp/signup.html')


            ref_code = create_refcode(name)
            user = User.objects.create_user(username = phonenumber, password = password, email = emailid, )
            user.save()
            userdetail_object = models.UserDetail(user = user, name = name, mobile = phonenumber, mailid = emailid, address = address, ref_code = ref_code)
            userdetail_object.save()



            return redirect('home')

    return render(request,'turfapp/signup.html')


def authenticator(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            authlogin(request, user)
            print('success')
            return redirect('home')
        else:
            print('error')
            messages.error(request, 'invalid username or password')
            return redirect('login')

@login_required
def user(request):

    print('user : ',request.user)
    userobj = models.UserDetail.objects.filter(user = request.user).first()
    print(userobj.name)
    if request.method == 'POST':
        address = request.POST['address']
        user_object = models.UserDetail.objects.filter(user = request.user).first()
        user_object.address = address
        user_object.save()
        print(address)
        return redirect('user')

    return render(request,'turfapp/user.html', {'userobj': userobj})

@login_required
def userbooking(request):

     current_time = datetime.datetime.now()
     current_booking = models.Booking.objects.filter(user = request.user, date__gte = current_time).order_by('-date')
     print(current_time)
     return render(request,'turfapp/userbooking.html', {'current_bookings': current_booking})

@login_required
def userhistory(request):
    current_time = datetime.datetime.now()
    current_history = models.Booking.objects.filter(user = request.user, date__lt = current_time)
    return render(request, 'turfapp/userhistory.html', {'current_history': current_history})

@login_required
def  userreferral(request):


    user_object = models.UserDetail.objects.filter(user = request.user).first()
    balance = user_object.coin_balance
    ref_code = user_object.ref_code
    referral = models.Referrals.objects.filter(parent = request.user)

    return render(request, 'turfapp/userreferral.html', {'ref_code': ref_code, 'referral': referral, 'balance': balance})

def  log_out_user(request):
    logout(request)

    return render(request, 'turfapp/index.html')

def cancel(request,pk):
    print('pk',pk)
    cancel_obj = models.Booking.objects.filter(id = pk).first()
    cancel_obj.delete()
    return redirect('userbooking')

def image(request):
    img_obj = models.Gallery.objects.all().order_by('-date')
    return render(request, 'turfapp/image.html',{'img_objs': img_obj})

def get_offeramount(offer_id, price):
    offer_object = models.Offer.objects.get(id=offer_id)
    if offer_object.is_percentage:
        offer_amount = price * offer_object.rate / 100
    else:
        offer_amount = offer_object.rate

    return offer_amount

def booking_check(slot, date):
    slot_det = models.Slot.objects.get(id=slot)
    try:
        date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    except:
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
    booking_obj = models.Booking.objects.filter(date=date, slot=slot_det)
    print('bookingobj*****', booking_obj)

    if len(booking_obj) > 0:
        return True
    else:
        False

@login_required
@cache_control(no_cache = True, must_revalidate = True , no_store = True)
def payment(request,slot,date,offer_id = 0):
    if booking_check(slot,date):
        return redirect('book')
    print('Date Format :' , date)
    print('*'*50)
    try:
        date = datetime.datetime.strptime(date,"%Y-%m-%d").strftime("%d-%m-%Y")
    except Exception as e:
        print('*'*10)
        print(date)
        date = datetime.datetime.strptime(date , "%d-%m-%Y").strftime('%Y-%m-%d')
        print(date)
        print('*' * 10)

    offer_obj = models.Offer.objects.filter(closed = False).order_by('-bdate')
    user_det = models.UserDetail.objects.filter(user = request.user).first()
    slot_det = models.Slot.objects.get(id = slot)
    settings = models.Settings.objects.first()
    maxcoin = settings.maxcoin
    one_coin = settings.one_coin
    coin_balance = user_det.coin_balance
    selected_offer = ''
    if offer_id > 0:
        offer_amount = get_offeramount(offer_id, slot_det.price)
        selected_offer = models.Offer.objects.get(id = offer_id)
    else:
        try:
            offer_amount = 0
            # offer_amount = get_offeramount(offer_obj[0].id, slot_det.price)
            # selected_offer = offer_obj[0]
        except:
            offer_amount = 0

    usable_coins = 0
    if coin_balance > maxcoin:
        usable_coins = maxcoin
    else:
        usable_coins = coin_balance

    usable_amount = usable_coins * one_coin
    total_amount = slot_det.price - usable_amount - offer_amount


    if request.method == 'POST':
        print('slot',slot_det)
        print('date:' , date)
        try:
            date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
        except:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
        booking_obj = models.Booking.objects.filter(date = date, slot = slot_det)
        print('bookingobj', booking_obj)

        if len(booking_obj) > 0:
            messages.error(request, 'Slot already booked')
            return redirect('payment', slot , date)
        booking_obj = models.Booking(
                                    user = request.user,
                                    slot = slot_det,
                                    date = date,
                                    amount = slot_det.price,
                                    coins_used = usable_coins,
                                    offer_applied = selected_offer.bname if selected_offer else '',
                                    offer_amount = offer_amount,
                                    total_amount = total_amount
                                    )
        booking_obj.save()
        return redirect('userbooking')





    return render(request, 'turfapp/payment.html',{'user_det': user_det, 'slot_det': slot_det,
                                                   'usable_amount': usable_amount, 'total_amount': total_amount,
                                                   'date': date, 'offer_objs': offer_obj, 'selected_offers': selected_offer,
                                                    'offer_amount': offer_amount})

def pricing(request):
    slot_object = models.Slot.objects.all().order_by('time')
    return render(request, 'turfapp/pricing.html', {'slot_objects': slot_object})

def feedback(request):
    feedback_obj = models.Feedback(feedback = request.POST, username = request.user)
    if request.method == 'POST':
        feedback_obj.feedback = request.POST['feedback']
        feedback_obj.save()
        return redirect('home')




    return render(request, 'turfapp/feedback.html', {'feedback_objs': feedback_obj})



