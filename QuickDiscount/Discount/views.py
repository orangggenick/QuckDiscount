from django.shortcuts import render

from Discount.models import Stock


def home(request):
    return render(request, 'Discount/index.html', {'stocks': Stock.objects.all()})
