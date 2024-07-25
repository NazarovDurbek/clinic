from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from users.forms import UserProfileForm, UserRegistrationForm, UserLoginForm
from users.utils.service import del_patient
from app.models import Order, TimeSlot

# Create your views here.






def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("index"))
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(request, "users/login.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request, 'users/singup.html', context)



@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    try: 
        timeslot = TimeSlot.objects.get(patient=request.user) 
    except TimeSlot.DoesNotExist: 
        timeslot = None
    context = {'form':form,
                'orders': Order.objects.filter(user=request.user).order_by('-id'),
                'timeslot': timeslot
                }
    return render(request, 'users/04.html', context)


def edit_status(request, status):
    slot = get_object_or_404(TimeSlot, patient=request.user)
    if status == 1:
        del_patient(slot.id)
        return HttpResponseRedirect(reverse('app:book_slot', kwargs={'doc_id': slot.doctor.id, 'type': slot.type}))
    del_patient(slot.id)
    return HttpResponseRedirect(reverse('users:profile'))





def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
