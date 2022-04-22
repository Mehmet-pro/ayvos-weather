from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Cities,Logs
from .forms import SignupForm,LoginForm,UpdateUserForm,CityUpdateForm
from .api import log
from django.db.models import Q
from datetime import datetime

@login_required
@csrf_exempt
def index(request):
    context = {}
    #post request for modify
    if request.POST and request.user.is_staff:
        city = request.POST.get('city')
        # delete - City
        if request.POST.get('delete'):
            Cities.objects.filter(city = city).delete()
            return redirect("index")
        #add - City
        if request.POST.get('add') and city:
            Cities.objects.create(city = city)

        if request.POST.get('add-user'):
            signupform = SignupForm(request.POST)
            if signupform.is_valid():
                signupform.save()
                raw_password = signupform.cleaned_data.get('password1')
                raw_username = signupform.cleaned_data.get('username')
                user = authenticate(request,username = raw_username,password=raw_password)
                login(request, user)
            else:
                messages.success(request,signupform.non_field_errors())
        
        if request.POST.get('save'):
            city_id = request.GET.get('c')
            if city_id:
                city_data = Cities.objects.get(city=city_id)
                modify_city = CityUpdateForm(request.POST,instance=city_data)
                if modify_city.is_valid():
                    modify_city.save()
                    return redirect("index")
    

        if request.POST.get('update-user'):
            user_id = request.GET.get('u')
            if user_id:
                user_ins = User.objects.get(id = user_id)
                user_update = UpdateUserForm(request.POST, instance=user_ins)
                if user_update.is_valid():
                    ## update password ##
                    ## search for update password and uncomment -> you need to uncomment things in forms.py too.
                    # password = request.POST.get('password')
                    # if password:
                    #     user_ins.set_password(password)
                    user_update.save()
            

        if request.POST.get('delete-user'):
            user_id = request.GET.get('u')
            User.objects.filter(id = user_id).delete()
            return redirect("index")

    if request.GET and request.user.is_staff:
        city_id = request.GET.get('c')
        if city_id:
            city_data = Cities.objects.get(city=city_id)
            context['city_modify_form'] = CityUpdateForm(instance=city_data)
        user_id = request.GET.get('u')
        if user_id:
            user_data = User.objects.get(id = user_id)
            context['update_user_from'] = UpdateUserForm(instance=user_data)
            
    if request.user.is_staff:
        context['signup_form'] = SignupForm()

    context['cities'] = Cities.objects.all()
    context['users'] = User.objects.all()
    return render(request,'index.html',context)

@login_required
def weather(request,city):
    context = {}
    context['cities'] = Cities.objects.all()
    context['w_data'] = log(request,city) #log() gets the data from api and register logs.
    return render(request,'weather.html',context)

@login_required
def log_view(request,user_id):
    context = {}
    logs = Logs.objects.filter(user_id = user_id).order_by("-log_date")
    if request.GET:
        time_from = request.GET.get('from')
        time_to = request.GET.get('till')
        if time_from and time_to:
            time_from = datetime.strptime(time_from,'%Y-%m-%dT%H:%M') #fromat html datetime-local
            time_to = datetime.strptime(time_to,'%Y-%m-%dT%H:%M')
            logs = logs.filter(
                Q(log_date__range = [time_from,time_to])
            )
        city = request.GET.get('city')
        state = request.GET.get('state')
        if state:
            if state == "succeed":
                state = True
            elif state == "failed":
                state = False
            
            logs = logs.filter(
                Q(response_state = state)
            )

        if city:
            if city == "None":
                logs = logs.filter(
                    Q(location_id__city__isnull = True)
                )
            else:
                logs = logs.filter(
                    Q(location_id__city = city)
                )

    context['filter'] = Logs.objects.filter(user_id = user_id).order_by("-log_date")
    context['logs'] = logs
    return render(request,'logs.html',context)


def handle_not_found(request,exception):
    return render(request,"not_found.html")


@csrf_exempt
def login_view(request):
    context = {}
    context['login_form'] = LoginForm()

    if request.POST:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            raw_password = loginform.cleaned_data.get('password')
            raw_username = loginform.cleaned_data.get('username')
            user = authenticate(request, username=raw_username, password=raw_password) #auth user
            if user is not None:
                login(request, user)
                next = request.GET.get('next')
                if next:   #if url has next page declared
                    return redirect(next)
                else:
                    return redirect('index')
        else:
            messages.success(request,"please check your info") #raise error when login faild

    return render(request,"login.html",context)

def logout_view(request):
    logout(request) #logout
    return redirect('login')