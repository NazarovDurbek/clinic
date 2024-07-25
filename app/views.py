from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from app.forms import OrderForm
from users.forms import UserProfileForm
from .models import AvailableDays, Contact, Hospital, Doctor, Language, TimeSlot, Product, Basket, Article
from .utils.paginator import paginate_objects
# Create your views here.








def index(request):
    return render(request, 'app/index.html')


def hospitals(request):
    city = request.GET.get('city', None)
    page = request.GET.get("page", 1)
    hospitals = Hospital.objects.all()
    if city:
        hospitals = hospitals.filter(city__name=city)
    hospitals = paginate_objects(objects=hospitals, page_number=page, per_page=10)
    return render(request, 'app/hospitals_list.html', {'hospitals': hospitals})


def hospital_detail(request, hospital_slug):
    hospital = get_object_or_404(Hospital, slug=hospital_slug)
    doctors = Doctor.objects.filter(hospital=hospital)
    hospital.visits += 1
    hospital.save()
    return render(request, 'app/hospital_detail.html', {'hos':hospital, 'doctors':doctors})



def doctors_list(request, doctor_specialty):
    languages = Language.objects.all()
    doctors = Doctor.objects.filter(specialty__name=doctor_specialty)
    page = request.GET.get("page", 1)
    selected_languages = request.POST.getlist('selected_languages', None)
    if selected_languages:
        doctors = doctors.filter(languages__name__in=selected_languages)
    doctors = paginate_objects(objects=doctors, page_number=page, per_page=10)
    context = {'doctors':doctors, 'specialty':doctor_specialty, 'languages':languages}
    return render(request, 'app/doctors_list.html', context)



def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.visits += 1
    doctor.save()
    doctors = Doctor.objects.filter(specialty__name=doctor.specialty).exclude(id=doctor.id)
    return render(request, 'app/doctor_detail.html', {'doctor':doctor, 'doctors':doctors})



@login_required
def book_slot(request, doc_id, type):
    available_slots = AvailableDays.objects.filter(time_slots__is_booked=False, time_slots__doctor_id=doc_id).order_by('date').distinct()
    if request.method == 'POST':
        try:
            selected_date = request.POST.get('selected_date')
            selected_time = request.POST.get('selected_time')
            time_slot = get_object_or_404(TimeSlot, available_slot__id=selected_date, time=selected_time)
            time_slot.is_booked = True
            time_slot.patient = request.user
            time_slot.type = type
            time_slot.save()
            return redirect(reverse('app:patient_details'))
        except IntegrityError:
            pass
    return render(request, 'app/01.html', {'available_slots': available_slots})




@login_required
def patient_details(request):
    slot = get_object_or_404(TimeSlot, patient=request.user)
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app:confirm_record'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form':form,
                'slot': slot
                }

    return render(request, 'app/record.html', context=context)




def goods(request):
    products = Product.objects.all()
    page = request.GET.get("page", 1)
    selected_categories = request.GET.getlist('selected_categories', None)
    if selected_categories:
        products = products.filter(category__name__in=selected_categories)
    products = paginate_objects(objects=products, page_number=page, per_page=12)
    context = {'products': products}
    return render(request, 'app/goods_list.html', context)



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.all().exclude(id=product_id)[:6]
    return render(request, 'app/product.html', {'product':product, 'products':products})



@login_required
def basket_add(request, product_id):
    quantity = int(request.POST.get("quantity", 1))
    product = Product.objects.get(id=product_id)
    if product.product_counts < quantity:
        quantity = product.product_counts
    Basket.objects.create(user=request.user, product=product, quantity=quantity, active=True)
    product.product_counts -= quantity
    product.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket(request):
    template = 'app/basket.html'
    baskets = Basket.objects.filter(user=request.user, active=True)
    if not baskets.exists():
        template = 'app/empty_basket.html'
    return render(request, template, {'baskets':baskets})

# @login_required
# def convert_baskets_to_order(request):
#     baskets = Basket.objects.filter(user=request.user, active=True)
#     total_price = baskets.total_sum() + baskets.total_tax() + 5
#     if request.method == 'POST':
#         order = Order.objects.create(user=request.user, 
#                                     total_price=total_price, 
#                                     receiver_address=request.POST.get('receiver_address'),
#                                     receiver_name=request.POST.get('receiver_name'), 
#                                     receiver_phone=request.POST.get('receiver_phone'), 
#                                     receiver_email=request.POST.get('receiver_email'),
#                                     receiver_surname=request.POST.get('receiver_surname'),
#                                     message=request.POST.get('message'),)
#         for basket in baskets:
#             order.baskets.add(basket)
#             basket.active = False
#             basket.save()
#             return HttpResponseRedirect(reverse('app:confirm_order'))
#     return render(request, 'app/order.html', {'baskets': baskets})



@login_required
def convert_baskets_to_order(request):
    baskets = Basket.objects.filter(user=request.user, active=True)
    total_price = baskets.total_sum() + baskets.total_tax() + 5 

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()
            order.baskets.set(baskets)
            baskets.update(active=False)  
            return redirect(reverse('app:confirm_order'))
    else:
        form = OrderForm()

    return render(request, 'app/order.html', {'baskets': baskets, 'form': form})

def confirm_order(request):
    return render(request, 'app/confirm_order.html')

def confirm_record(request):
    return render(request, 'app/confirm_record.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        text = request.POST.get('text')
        contact = Contact(name=name, email=email, phone=phone, text=text)
        contact.save()
        return HttpResponseRedirect('/')
    return render(request, 'app/contact.html')



def novosti_catalog(request):
    page = request.GET.get("page", 1)
    selected_categories = request.GET.getlist('selected_categories', None)
    articles = Article.objects.all()
    if selected_categories:
        articles = articles.filter(category__name__in=selected_categories)
    articles = paginate_objects(objects=articles, page_number=page, per_page=12)
    context = {'articles': articles}
    return render(request, 'app/novosti_catalog.html', context)



def o_nas(request):
    return render(request, 'app/o_sebe.html')