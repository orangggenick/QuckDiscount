from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf

from Discount.models import Stock, DiscountUserForm


def home(request):
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
