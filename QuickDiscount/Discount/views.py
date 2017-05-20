from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf

from Discount.models import Stock, DiscountUserForm, DiscountUser, Shop, ShopForm


def home(request):
    if auth.get_user(request).id != None:
        user = auth.get_user(request)
        status = user.discountuser.status
        if status == 'stuff':
            return render(request, 'Discount/myshops.html', {'shops': Shop.objects.filter(seller_id = auth.get_user(request).id)})
        else:
            return render(request, 'Discount/index.html', {'stocks': Stock.objects.all()})
    else:
        return render(request, 'Discount/index.html', {'stocks': Stock.objects.all()})


def registration_step1(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = auth.authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password2'])
            auth.login(request, user)
            return redirect('/complete_registration')
        else:
            args['form'] = user_form
    return render_to_response('Discount/registration.html', args)


def registration_step2(request):
    if auth.get_user(request).id != None:
        args = {}
        args.update(csrf(request))
        args['form'] = DiscountUserForm()
        if request.POST:
            user_form = DiscountUserForm(request.POST)
            if user_form.is_valid():
                buffer = user_form.save(commit=False)
                buffer.user = auth.get_user(request)
                user_form.save()
                return redirect('/')
            else:
                args['form'] = user_form
        return render_to_response('Discount/registration2.html', args)
    else:
        return redirect('/sign_up')


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден!"
            return render_to_response('Discount/login.html', args)
    else:
        return render_to_response('Discount/login.html', args)

def logout(request):
    auth.logout(request)
    return redirect("/")


def shops(request):
    return render(request, 'Discount/shops.html', {'shops': Shop.objects.all()})


def add_shop(request):
    if auth.get_user(request).id != None:
        args = {}
        args.update(csrf(request))
        args['form'] = ShopForm()
        if request.POST:
            user_form = ShopForm(request.POST)
            if user_form.is_valid():
                buffer = user_form.save(commit=False)
                buffer.seller_id = auth.get_user(request).id
                user_form.save()
                return redirect('/')
            else:
                args['form'] = user_form
        return render_to_response('Discount/add_shop.html', args)
    else:
        return redirect('/login')