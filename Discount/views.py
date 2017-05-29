from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf

from Discount.models import Stock, DiscountUserForm, DiscountUser, Shop, ShopForm, StockForm, \
    Subscription, DiscountUserForm2, ShopForm2, Favorites


def home(request):
    """Вызов стартовой страницы

    Parameter
       request.GET '/'

    Return
       home page with list of active stocks
       or
       home page with list of active stocks and list of favorite stocks
    """
    if auth.get_user(request).id != None:
        favorites = Favorites.objects.filter(user_id=auth.get_user(request).id)
        stocks_ids = []
        for favorite in favorites:
            stocks_ids.append(favorite.stock_id)
        return render(request, 'Discount/index.html', {'stocks': Stock.objects.filter(is_active=True), 'favorite_ids': stocks_ids})
    else:
        return render(request, 'Discount/index.html', {'stocks': Stock.objects.filter(is_active=True)})


def registration_step1(request):
    """Регистрация пользователя (шаг 1)

    Parameter
        request.GET '/sign_up' or request.POST '/sign_up'

    Return
        registration page with form
        or
        registration page with form and errors
        or
        redirect to complete registration
    """
    # :return html registration with form or redirect to complete registration
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
    """Регистрация пользователя (шаг 2)

    Parameter
        request.GET '/complete_registration' or request.POST '/complete_registration'

    Return
        complete registration page with form
        or
        complete registration page with form and errors
        or
        redirect to home page
    """
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
    """Авторизация пользователя

    Parameter
        request.GET '/login' or request.POST '/login'

    Return
        login page with form
        or
        login page with form and errors
        or
        redirect to home page
    """
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
    """Выход пользователя из аккаунта

    Parameter
        request.GET '/logout'

    Return
        redirect to home page
    """
    auth.logout(request)
    return redirect("/")


def shops(request):
    """Получение списка магазинов

    Parameter
        request.GET '/shops'

    Return
        shops page with the list of all shops
    """
    subscriptions = Subscription.objects.filter(user_id=auth.get_user(request).id)
    shop_ids = []
    for subscription in subscriptions:
        shop_ids.append(subscription.shop_id)
    return render(request, 'Discount/shops.html', {'shops': Shop.objects.all(), 'shop_ids': shop_ids})


def add_shop(request):
    """Добавление магазина

    Parameter
        request.GET '/add_shop'
        or
        request.POST '/add_shop'

    Return
        add shop page with form or add shop page with form and errors or redirect to home page or redirect to login
    """
    if auth.get_user(request).id != None:
        args = {}
        args.update(csrf(request))
        args['form'] = ShopForm()
        if request.POST:
            user_form = ShopForm(request.POST, request.FILES)
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


def shop(request, shop_id):
    """Просмотр акций конкретного магазина

    Parameters
        request.GET '/shop' and int shop_id

    Return
        shop page with Shop object (id=shop_id) and list of it's stocks
        or
        shop page with Shop object (id=shop_id) and list of it's stocks and list of subscriptions of user and list of favorite stocks of user
    """
    subscriptions = Subscription.objects.filter(user_id=auth.get_user(request).id)
    shop_ids = []
    for subscription in subscriptions:
        shop_ids.append(subscription.shop_id)
    favorites = Favorites.objects.filter(user_id=auth.get_user(request).id)
    stocks_ids = []
    for favorite in favorites:
        stocks_ids.append(favorite.stock_id)
    return render(request, 'Discount/shop.html', {'stocks': Stock.objects.filter(shop_id = shop_id), 'shop': Shop.objects.get(id=shop_id), 'shop_ids': shop_ids, 'favorite_ids': stocks_ids})


def add_stock(request, shop_id):
    """Добавление акции

    Parameters
        request.GET '/add_stock' and int shop_id

    Return
        add shop page with form
        or
        add shop page with form and errors
        or
        redirect to home page
        or
        redirect to login
    """
    shop = Shop.objects.get(id = shop_id)
    if auth.get_user(request).id == shop.seller_id:
        args = {}
        args.update(csrf(request))
        args['form'] = StockForm()
        args['shop'] = Shop.objects.get(id=shop_id)
        if request.POST:
            stock_form = StockForm(request.POST)
            if stock_form.is_valid():
                buffer = stock_form.save(commit=False)
                buffer.is_active = True
                buffer.shop_id = shop_id
                stock_form.save()
                return redirect('/')
            else:
                args['form'] = stock_form
        return render_to_response('Discount/add_stock.html', args)
    else:
        return redirect('/login')


def subscribe(request, shop_id):
    """Выполнение подписки на магазин

    Parameters
        request.GET '/subscribe' and int shop_id

    Return
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        subscription = Subscription()
        subscription.user_id = auth.get_user(request).id
        subscription.shop_id = shop_id
        print(subscription.shop_id)
        subscription.save()
        return redirect('/')
    else:
        return redirect('/login')


def unsubscribe(request, shop_id):
    """Выполение отписки от акций магазина

    Parameters
        request.GET '/unsubscribe' and int shop_id

    Return
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        query = Subscription.objects.filter(user_id = auth.get_user(request).id)
        query.get(shop_id = shop_id).delete()
        return redirect('/')
    else:
        return redirect('/login')


def myshops(request):
    """Получение списка магазинов, которыми владеет пользователь

    Parameter
        request.GET '/myshops'

    Return
        my shops page with list of user's shops
        or
        redirect to home page
    """
    if auth.get_user(request).id != None:
        user = auth.get_user(request)
        status = user.discountuser.status
        if status == 'stuff':
            return render(request, 'Discount/myshops.html', {'shops': Shop.objects.filter(seller_id = auth.get_user(request).id)})
        else:
            return redirect('/')
    else:
        return redirect('/')


def mysubscripthons(request):
    """Получение списка акций от магазинов, на которые подписан пользователь

    Parameter
        request.GET '/mysubscripthons'

    Return
        my subscripthons page with list of stocks from favorite shops of user
        or
        redirect to home page
    """
    if auth.get_user(request).id != None:
        subscriptions = Subscription.objects.filter(user_id=auth.get_user(request).id)
        buffer = []
        for subscription in subscriptions:
            buffer.append(Stock.objects.filter(shop_id=subscription.shop_id))
        stocks = []
        for set in range(len(buffer)):
            for stock in range(len(buffer[set])):
                stocks.append(buffer[set][stock])
        favorites = Favorites.objects.filter(user_id=auth.get_user(request).id)
        stocks_ids = []
        for favorite in favorites:
            stocks_ids.append(favorite.stock_id)
        return render(request, 'Discount/mysubscripthons.html', {'stocks': stocks, 'favorite_ids': stocks_ids})
    else:
        return redirect('/')


def cabinet(request):
    """Редактирование профиля пользователя

    Parameter
        request.GET '/cabinet' or request.POST '/cabinet'

    Return
        cabinet page with form
        or
        cabinet page with form and errors
        or
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        user = DiscountUser.objects.get(user = auth.get_user(request))
        args = {}
        args.update(csrf(request))
        args['form'] = DiscountUserForm2
        args['user'] = user
        if request.POST:
            form = DiscountUserForm2(request.POST)
            if form.is_valid():
                buffer = form.save(commit=False)
                user.name = buffer.name
                user.surname = buffer.surname
                user.patronymic = buffer.patronymic
                user.phone = buffer.phone
                user.email = buffer.email
                user.categories = buffer.categories
                user.save()
                return redirect('/')
            else:
                args['form'] = DiscountUserForm2
        return render_to_response('Discount/cabinet.html', args)
    else:
        return redirect('/login')


def change_logo(request, shop_id):
    """Изменеие логотипа магазина

    Parameter
        request.GET '/change_logo' or request.POST '/change_logo' and int shop_id

    Return
        change logo page with form
        or
        change logo page with form and errors
        or
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        shop = Shop.objects.get(id=shop_id)
        if auth.get_user(request).id == shop.seller_id:
            args = {}
            args.update(csrf(request))
            args['form'] = ShopForm2
            args['shop'] = shop
            if request.POST:
                form = ShopForm2(request.POST, request.FILES)
                if form.is_valid():
                    buffer = form.save(commit=False)
                    shop.image = buffer.image
                    shop.save()
                    return redirect('/')
                else:
                    args['form'] = ShopForm2
            return render_to_response('Discount/change_logo.html', args)
        else:
            return redirect('/')
    else:
        return redirect('/login')


def change_stock(request, stock_id):
    """Редактирование акции

    Parameter
        request.GET '/change_stock' or request.POST '/change_stock' and int stock_id

    Return
        change stock page with form
        or
        change stock page with form and errors
        or
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        stock = Stock.objects.get(id=stock_id)
        shop = Shop.objects.get(id = stock.shop_id)
        if auth.get_user(request).id == shop.seller_id:
            args = {}
            args.update(csrf(request))
            args['form'] = StockForm
            args['shop'] = shop
            args['stock'] = stock
            if request.POST:
                form = StockForm(request.POST)
                if form.is_valid():
                    buffer = form.save(commit=False)
                    stock.exposition = buffer.exposition
                    stock.description = buffer.description
                    stock.terms = buffer.terms
                    stock.save()
                    return redirect('/shop/' + str(shop.id))
                else:
                    args['form'] = StockForm
            return render_to_response('Discount/change_stock.html', args)
        else:
            return redirect('/')
    else:
        return redirect('/login')


def delete_stock(request, stock_id):
    """Удаление акции

    Parameter
        request.GET '/delete_stock'

    Return
        redirect to current shop page
        or
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        stock = Stock.objects.get(id=stock_id)
        shop = Shop.objects.get(id = stock.shop_id)
        if auth.get_user(request).id == shop.seller_id:
            stock.delete()
            shop = Shop.objects.get(id=stock.shop_id)
            return redirect('/shop/' + str(shop.id))
        else:
            return redirect('/')
    else:
        return redirect('/login')


def add_to_favorites(request, stock_id):
    """Добавление акции в избранное

    Parameter
        request.GET '/add_to_favorites'

    Return
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        favourite = Favorites()
        favourite.user_id = auth.get_user(request).id
        favourite.stock_id = stock_id
        favourite.save()
        return redirect('/')
    else:
        return redirect('/login')


def delete_from_favorites(request, stock_id):
    """Удаление акции из избранного

    Parameter
        request.GET '/delete_from_favorites'

    Return
        redirect to home page
        or
        redirect to login
    """
    if auth.get_user(request).id != None:
        query = Favorites.objects.filter(user_id=auth.get_user(request).id)
        query.get(stock_id=stock_id).delete()
        return redirect('/')
    else:
        return redirect('/login')


def myfavorites(request):
    """Получение списка избранных акций пользователя

    Parameter
        request.GET '/myfavorites'

    Return
        my favorites page with list of favorite stocks of user
        or
        redirect to home page
    """
    if auth.get_user(request).id != None:
        favorites = Favorites.objects.filter(user_id=auth.get_user(request).id)
        buffer = []
        for favorite in favorites:
            buffer.append(Stock.objects.get(id=favorite.stock_id))
        return render(request, 'Discount/myfavorites.html', {'stocks': buffer})
    else:
        return redirect('/')